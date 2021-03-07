# -*- coding: utf-8 -*-
from decimal import Decimal

from core.models import MixeurBaseModel
from django.core.validators import MinValueValidator
from django.db import models


class YearlyEnergyPrice(MixeurBaseModel):
    class Meta:
        verbose_name = "Prix des énergies par année"
        unique_together = ("year", "energy")

    year = models.PositiveSmallIntegerField(verbose_name="Année")

    energy = models.ForeignKey(
        "energies.Energy",
        verbose_name="Énergie",
        on_delete=models.CASCADE,
        related_name="yearly_energy_price",
    )

    price = models.DecimalField(
        verbose_name="Prix",
        validators=(MinValueValidator(Decimal("1")),),
        max_digits=20,
        decimal_places=2,
        null=True,
    )
