from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.utils import timezone


COLOR_RESET = "\u001b[0m"
COLOR_BLUE = f"{COLOR_RESET}\u001b[34m"
COLOR_YELLOW = f"{COLOR_RESET}\u001b[33m"


# https://stackoverflow.com/a/3330128
class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()


class MixeurBaseModel(models.Model):
    """
    Mixeur base model which have default created_at and updated_at DateTimeField

    created_at: now on model's creation
    updated_at: change to now on model's update
    __repr__: explicit model representation
    """

    class Meta:
        abstract = True

    # https://stackoverflow.com/a/3330128
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    updated_at = AutoDateTimeField(editable=False, default=timezone.now)

    def __repr__(self):  # NOQA: C901
        values = [
            f"--{COLOR_YELLOW}{self.__class__}{COLOR_RESET} / {self.__class__.__name__.split('.')[-1]}.objects.get(pk={self.pk}) --------"  # NOQA: E501
        ]
        if f"{self.__class__}".endswith("QuerySet'>"):
            for v in self:
                values.append(f"{COLOR_RESET}{v}")
        else:
            for f in [x.name for x in self._meta.get_fields()]:
                try:
                    if hasattr(getattr(self, f"{f}_set"), "all"):
                        values.append(
                            f"  {COLOR_BLUE}{f}:{COLOR_RESET} M2M_set: {[x.pk for x in getattr(self, f'{f}_set').all()]}"  # NOQA: E501
                        )
                except AttributeError:
                    try:
                        if hasattr(getattr(self, f), "all"):
                            values.append(
                                f"  {COLOR_BLUE}{f}:{COLOR_RESET} M2M: {[x.pk for x in getattr(self, f).all()]}"
                            )

                        elif hasattr(getattr(self, f), "pk"):
                            values.append(
                                f"  {COLOR_BLUE}{f}:{COLOR_RESET} FK:{getattr(self, f).__class__}:{getattr(self, f).pk}"
                            )

                        elif hasattr(getattr(self.__class__, f), "field_name"):
                            value = getattr(self, f)
                            if isinstance(value, str):
                                value = value.replace("\n", "\\n")
                            values.append(f"  {COLOR_BLUE}{f}:{COLOR_RESET} {value}")
                    except AttributeError:
                        values.append(f"{f}: cannot get value")
                    except FieldDoesNotExist:
                        values.append(f"{f}: cannot get value (FieldDoesNotExist)")
                    except ValueError:
                        values.append(f"{f}: cannot get value (ValueError)")

        values.append(
            f"{COLOR_RESET}--/{self.__class__} / {self.__class__.__name__.split('.')[-1]}.objects.get(pk={self.pk}) -------"  # NOQA: E501
        )
        return "\n".join(values)
