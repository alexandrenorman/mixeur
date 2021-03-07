# -*- coding: utf-8 -*-

import datetime
import json
import logging

import html2text


logger = logging.getLogger(__name__)  # NOQA


class DataAdapter:
    class DataAdapterError(Exception):
        pass

    def __init__(self, adapters: dict = None):
        self.adapters = self._join_class_and_custom_function_adapters(adapters=adapters)

    def convert(self, rows: list, columns: dict, list_separator: str = ", "):
        converted_rows = self._apply_adapters_to_data(
            columns=columns,
            rows=rows,
            list_separator=list_separator,
            adapters=self.adapters,
        )
        return converted_rows

    @classmethod
    def _apply_adapters_to_data(
        cls, columns, rows, list_separator: str = ", ", adapters: dict = None
    ):
        for row in rows:
            for column in columns:
                fct = column["fct"] if "fct" in column else None
                if fct:
                    arg = column["arg"] if "arg" in column else None
                    default = column["default "] if "default" in column else None
                    row[column["field"]] = adapters[fct](
                        value=row[column["field"]],
                        arg=arg,
                        default=default,
                        list_separator=list_separator,
                    )

        return rows

    @staticmethod
    def _convert_bool(value, arg, *args, **kwargs):
        if type(value) is not bool:
            raise DataAdapter.DataAdapterError(f"value: {value} must be a boolean")

        return DataAdapter._convert_list(value, arg)

    @staticmethod
    def _convert_date(value, arg, default=None, *args, **kwargs):
        """
        - value: datetime
        - arg: format string as in https://docs.python.org/fr/3/library/datetime.html#strftime-and-strptime-format-codes
        """
        try:
            return value.strftime(arg)
        except ValueError:
            if default is not None:
                return datetime.datetime.strptime(default, arg)

            raise DataAdapter.DataAdapterError(
                f"value:{value} is not a valid date and default is not defined"
            )
        except AttributeError:
            if default is not None:
                return datetime.datetime.strptime(default, arg)

            return ""

    @staticmethod
    def _convert_fixed(arg, *args, **kwargs):
        return arg

    @staticmethod
    def _convert_float(value, default=None, *args, **kwargs):
        try:
            return float(value.replace(",", "."))
        except ValueError:
            if default is not None:
                return float(default)

            raise DataAdapter.DataAdapterError(
                f"value:{value} is not a float and default is not defined"
            )

    @staticmethod
    def _convert_html(value, arg=None, default=None, *args, **kwargs):
        ret = ""
        if value is not None:
            if arg:
                ret = DataAdapter._convert_truncate(
                    value=html2text.html2text(str(value)).replace("\n", " "),
                    arg=arg,
                    default=default,
                ).strip()
            else:
                ret = html2text.html2text(str(value)).replace("\n", " ").strip()

        return ret

    @staticmethod
    def _convert_int(value, default=None, *args, **kwargs):
        try:
            return int(value)
        except ValueError:
            if default is not None:
                return int(default)

            raise DataAdapter.DataAdapterError(
                f"value:{value} is not an int and default is not defined"
            )

    @staticmethod
    def _convert_list(value, arg, default=None, *args, **kwargs):
        # return key by value in dict
        if value is None or value == "":
            return ""
        try:
            return arg[value]
        except KeyError:
            if default is not None:
                return default

            raise DataAdapter.DataAdapterError(f"value:{value} not in {arg}")
        except ValueError:
            if default is not None:
                return default

            raise DataAdapter.DataAdapterError(f"value:{value} not in {arg}")

    @staticmethod
    def _convert_list_multiple(
        value, arg, default=None, list_separator=", ", *args, **kwargs
    ):
        # return list of keys by value in dict
        if value is None or value == [] or value == "":
            return ""

        returned_values = []
        try:
            values = json.loads(value)
        except TypeError:
            values = value

        for item in values:
            if item not in arg.keys():
                if default is not None:
                    returned_values = [default]
                else:
                    raise DataAdapter.DataAdapterError(f"value:{item} not in {arg}")

        for k in arg.keys():
            if k in value:
                returned_values.append(arg[k])

        return list_separator.join(returned_values)

    @staticmethod
    def _convert_nop(value, *args, **kwargs):
        return value

    @staticmethod
    def _convert_truncate(value, arg=None, *args, **kwargs):
        if value is not None:
            if arg is not None:
                return str(value)[:arg]
            else:
                return str(value)

        return ""

    @classmethod
    def _join_class_and_custom_function_adapters(cls, adapters: dict = None):
        adapters = adapters if adapters is not None else {}

        function_adapters = {
            "bool": cls._convert_bool,
            "date": cls._convert_date,
            "fixed": cls._convert_fixed,
            "float": cls._convert_float,
            "html": cls._convert_html,
            "int": cls._convert_int,
            "list": cls._convert_list,
            "list_multiple": cls._convert_list_multiple,
            "nop": cls._convert_nop,
            "truncate": cls._convert_truncate,
        }

        for function in adapters:
            function_adapters[function] = adapters[function]

        return function_adapters
