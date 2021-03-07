from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from core.models import MixeurBaseModel


class CarbonTax(MixeurBaseModel):
    class Meta:
        verbose_name = "Taxe carbone"

    year = models.IntegerField(("Année"), validators=(MinValueValidator(2018),))

    amount = models.DecimalField(
        verbose_name="Montant HT / tCO2",
        validators=(MinValueValidator(Decimal("1")),),
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return self.name
