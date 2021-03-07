from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from core.models import MixeurBaseModel


class SecondaryEfficiency(MixeurBaseModel):
    class Meta:
        verbose_name = "Rendement secondaire"

    is_heating = models.BooleanField(verbose_name="Chauffage ?", default=False)
    is_multi_unit = models.BooleanField(verbose_name="Collectif ?", default=False)
    is_hydro = models.BooleanField(verbose_name="With hydrolic system ?", default=True)

    ratio = models.DecimalField(
        max_digits=13,
        decimal_places=10,
        default=0,
        verbose_name="Ratio",
        validators=(MinValueValidator(Decimal("0")),),
    )

    @classmethod
    def get(cls, is_heating, is_multi_unit, is_hydro=True):
        if is_multi_unit:
            secondary_efficiency = cls.objects.filter(
                is_heating=is_heating, is_multi_unit=is_multi_unit
            ).first()
        else:
            secondary_efficiency = cls.objects.filter(
                is_heating=is_heating, is_multi_unit=is_multi_unit, is_hydro=is_hydro
            ).first()

        return secondary_efficiency.ratio if secondary_efficiency else Decimal("1")
