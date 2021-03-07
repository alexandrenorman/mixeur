# -*- coding: utf-8 -*-
from django.core.exceptions import FieldDoesNotExist


class UniversalReprMixin:
    def __repr__(self):  # NOQA: C901
        values = [f"--{self.__class__}--------"]
        if f"{self.__class__}".endswith("QuerySet'>"):
            for v in self:
                values.append(f"{v}")
        else:
            for f in dir(self.__class__):
                if f in [
                    "objects",
                    "DoesNotExist",
                    "Meta",
                    "MultipleObjectsReturned",
                    "REQUIRED_FIELDS",
                    "USERNAME_FIELD",
                    "__class__",
                    "__delattr__",
                    "__dict__",
                    "__dir__",
                    "__doc__",
                    "__eq__",
                    "__format__",
                    "__ge__",
                    "__getattribute__",
                    "__gt__",
                    "__hash__",
                    "__init__",
                    "__init_subclass__",
                    "__le__",
                    "__lt__",
                    "__module__",
                    "__ne__",
                    "__new__",
                    "__reduce__",
                    "__reduce_ex__",
                    "__repr__",
                    "__setattr__",
                    "__setstate__",
                    "__sizeof__",
                    "__str__",
                    "__subclasshook__",
                    "__weakref__",
                    "_check_column_name_clashes",
                    "_check_field_name_clashes",
                    "_check_fields",
                    "_check_id_field",
                    "_check_index_together",
                    "_check_local_fields",
                    "_check_long_column_names",
                    "_check_m2m_through_same_relationship",
                    "_check_managers",
                    "_check_model",
                    "_check_model_name_db_lookup_clashes",
                    "_check_ordering",
                    "_check_swappable",
                    "_check_unique_together",
                    "_do_insert",
                    "_do_update",
                    "_get_FIELD_display",
                    "_get_next_or_previous_by_FIELD",
                    "_get_next_or_previous_in_order",
                    "_get_pk_val",
                    "_get_unique_checks",
                    "_meta",
                    "_perform_date_checks",
                    "_perform_unique_checks",
                    "_save_parents",
                    "_save_table",
                    "_set_pk_val",
                    "delete",
                    "save",
                    "serializable_value",
                ]:
                    continue

                try:
                    if False and hasattr(getattr(self, f), "all"):
                        values.append(
                            f"{f}: M2M: {[x.pk for x in getattr(self, f).all()]}"
                        )

                    elif hasattr(getattr(self, f), "pk"):
                        values.append(
                            f"{f}: FK:{getattr(self, f).__class__}:{getattr(self, f).pk}"
                        )

                    elif hasattr(getattr(self.__class__, f), "field_name"):
                        values.append(f"{f}: {getattr(self, f)}")
                except AttributeError:
                    values.append(f"{f}: cannot get value")
                except FieldDoesNotExist:
                    values.append(f"{f}: cannot get value (FieldDoesNotExist)")
                except ValueError:
                    values.append(f"{f}: cannot get value (ValueError)")

        values.append(f"--/{self.__class__}-------")
        return "\n".join(values)
