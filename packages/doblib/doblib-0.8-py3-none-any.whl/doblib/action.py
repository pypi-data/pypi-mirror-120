# © 2021 Florian Kantelberg (initOS GmbH)
# License Apache-2.0 (http://www.apache.org/licenses/).

import random
import string
import uuid
from datetime import date, datetime, timedelta

from . import base, env, utils

ALNUM = string.ascii_letters + string.digits


def load_action_arguments(args, actions=None):
    parser = utils.default_parser("action")
    parser.add_argument(
        "action",
        metavar="action",
        choices=actions or (),
        help=f"Action to run. Possible choices: {','.join(actions)}",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Run the action as a dry-run and don't commit changes",
    )
    return parser.parse_known_args(args)


class ActionEnvironment(env.Environment):
    """ Class to apply actions in the environment """

    def _apply(self, rec, name, **kw):
        """ Apply an action on a field of a record """
        field_type = rec._fields[name].type
        if field_type == "boolean":
            return self._boolean(rec, name=name, **kw)
        if field_type == "integer":
            return self._integer(rec, name=name, **kw)
        if field_type in ("float", "monetary"):
            return self._float(rec, name=name, **kw)
        if field_type == "date":
            return self._date(rec, name=name, **kw)
        if field_type == "datetime":
            return self._datetime(rec, name=name, **kw)
        if field_type in ("char", "html", "text"):
            return self._text(rec, name=name, **kw)
        raise TypeError("Field type is not supported by action handler")

    def _boolean(self, rec, **kw):
        """Return a value for boolean fields depending on the arguments

        * Take the value from a field of the record and interpret as boolean
        * Randomly True or False
        """
        field = kw.get("field")
        # Use the value of a different field
        if field:
            return bool(rec[field])

        return random.choice((False, True))

    def _integer(self, rec, **kw):
        """Return a value for integer fields depending on the arguments

        * Take the value from a `field` of the record
        * Random value between `lower` and `upper`
        """

        lower = kw.get("lower", None)
        upper = kw.get("upper", None)
        field = kw.get("field", None)
        # Use the value of a different field
        if field:
            return rec[field]

        # Randomize the value
        if isinstance(lower, int) and isinstance(upper, int):
            return random.randint(lower, upper)

        raise TypeError("Lower and upper bounds must be integer")

    def _float(self, rec, **kw):
        """Return a value for float fields depending on the arguments

        * Take the value from a `field` of the record
        * Random value between `lower` and `upper`
        """
        lower = kw.get("lower", 0.0)
        upper = kw.get("upper", 1.0)
        field = kw.get("field", None)
        # Use the value of a different field
        if field:
            return rec[field]

        # Randomize the value
        return random.random() * (upper - lower) + lower

    def _text(self, rec, **kw):
        """Return a value for text fields depending on the arguments

        * Generate a UUID if `uuid` is set. Support UUID1 and UUID4
        * Take the value from a `field` of the record. Add `prefix` and `suffix`
        * Random alphanumeric string with specific `length`. Add `prefix` and `suffix`
        * Current value of the field with `prefix` and `suffix` added
        """
        prefix = kw.get("prefix", "")
        suffix = kw.get("suffix", "")
        length = kw.get("length", None)
        field = kw.get("field", None)
        vuuid = kw.get("uuid", None)
        # Support for uuid1 and uuid4
        if vuuid == 1:
            return str(uuid.uuid1())
        if vuuid == 4:
            return str(uuid.uuid4())

        # Use the value of a different field
        if isinstance(field, str):
            return f"{prefix}{rec[field]}{suffix}"

        # Randomize the value
        if isinstance(length, int) and length > 0:
            return prefix + "".join(random.choices(ALNUM, k=length)) + suffix

        return prefix + rec[kw["name"]] + suffix

    def _datetime(self, rec, **kw):
        """Return a value for datetime fields depending on the arguments

        * Take the value from a `field` of the record
        * Random value between `lower` and `upper`
        """
        lower = kw.get("lower", datetime(1970, 1, 1))
        upper = kw.get("upper", datetime.now())
        field = kw.get("field", None)
        if field:
            return rec[field]

        diff = upper - lower
        return lower + timedelta(seconds=random.randint(0, diff.seconds))

    def _date(self, rec, **kw):
        """Return a value for date fields depending on the arguments

        * Take the value from a `field` of the record
        * Random value between `lower` and `upper`
        """
        lower = kw.get("lower", date(1970, 1, 1))
        upper = kw.get("upper", date.today())
        field = kw.get("field", None)
        if field:
            return rec[field]

        return lower + timedelta(days=random.randint(0, (upper - lower).days))

    def _replace_references(self, env, references, values):
        resolved_refs = {}
        for key, val in references.items():
            resolved_refs[key] = env.ref(val).id

        self._replace_recursively(values, resolved_refs)

    def _replace_recursively(self, value, replace_dict):
        if isinstance(value, dict):
            iterator = value
        elif isinstance(value, list):
            iterator = range(0, len(value))
        else:
            return

        for index in iterator:
            if isinstance(value[index], str):
                if value[index] in replace_dict:
                    value[index] = replace_dict[value[index]]
            else:
                self._replace_recursively(value[index], replace_dict)

    def _action_delete(self, env, model, domain, references):
        """ Runs the delete action """
        if model in env:
            self._replace_references(env, references, domain)
            env[model].with_context(active_test=False).search(domain).unlink()

    def _action_update(self, env, model, domain, references, values):
        """ Runs the update action """
        if not values or model not in env:
            return

        self._replace_references(env, references, domain)
        self._replace_references(env, references, values)

        records = env[model].with_context(active_test=False).search(domain)

        # Split the values in constant and dynamic
        const, dynamic = {}, {}
        for name, apply_act in values.items():
            if name not in records._fields:
                continue

            if isinstance(apply_act, dict):
                dynamic[name] = apply_act
            else:
                const[name] = apply_act

        # Handle the constant values
        if const:
            records.write(const)

        # Handle the dynamic values
        if dynamic:
            for rec in records:
                vals = {}
                for name, apply_act in dynamic.items():
                    vals[name] = self._apply(rec, name, **apply_act)
                rec.write(vals)

    def _action_insert(self, env, model, domain, references, values):
        if not domain or not values or model not in env or env[model].search(domain):
            return

        self._replace_references(env, references, domain)
        self._replace_references(env, references, values)

        env[model].with_context(active_test=False).create(values)

    def apply_action(self, args=None):
        """ Apply in the configuration defined actions on the database """
        actions = self.get("actions", default={})
        args, _ = load_action_arguments(args or [], list(actions))

        if not self._init_odoo():
            return

        # pylint: disable=C0415,E0401
        import odoo
        from odoo.tools import config

        # Load the Odoo configuration
        config.parse_config(["-c", base.ODOO_CONFIG])
        odoo.cli.server.report_configuration()

        db_name = config["db_name"]

        utils.info(f"Running {args.action}")
        with odoo.api.Environment.manage():
            with self.env(db_name) as env:
                for name, item in actions[args.action].items():
                    utils.info(f"{args.action.capitalize()} {name}")
                    model = item.get("model")
                    if not isinstance(model, str):
                        utils.error("Model must be string")
                        continue

                    domain = item.get("domain", [])
                    if not isinstance(domain, list):
                        utils.error("Domain must be list")
                        continue

                    act = item.get("action", "update")
                    references = item.get("references", {})
                    if act == "update":
                        values = item.get("values", {})
                        self._action_update(env, model, domain, references, values)
                    elif act == "delete":
                        self._action_delete(env, model, domain, references)
                    elif act == "insert":
                        values = item.get("values", {})

                        self._action_insert(env, model, domain, references, values)
                    else:
                        utils.error(f"Undefined action {act}")
