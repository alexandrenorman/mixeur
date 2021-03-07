# -*- coding: utf-8 -*-
from decimal import Decimal
from django.db import models
from core.models import MixeurBaseModel

from django.utils.translation import ugettext_lazy as _

from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


# leaves function to not break migrations
def validation_absolute_positive(value):
    if value < 1:
        raise ValidationError(f"Value must be > 1 (was {value}")


class YearlyData(MixeurBaseModel):
    class Meta:
        ordering = ("-years",)
        verbose_name = _("Données annuelle")

    copro = models.ForeignKey(
        "autodiag_copro.Copro",
        related_name="yearly_data",
        verbose_name=_("Copropriété"),
        on_delete=models.CASCADE,
    )

    years = models.CharField(_("Années"), max_length=9)

    # HEATING
    heating_energy_charges = models.DecimalField(
        _("Énergie - chauffage"),
        validators=(MinValueValidator(Decimal("0")),),
        max_digits=20,
        decimal_places=2,
    )
    energy_consumption = models.DecimalField(
        _("Énergie brute"),
        validators=(MinValueValidator(Decimal("0")),),
        max_digits=20,
        decimal_places=2,
    )
    # HOTWATER
    hot_water_energy_charges = models.DecimalField(
        _("Énergie - eau chaude"),
        validators=(MinValueValidator(Decimal("0")),),
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
    )
    hot_water_consumption_charges = models.DecimalField(
        _("Consommation - eau chaude"),
        validators=(MinValueValidator(Decimal("0")),),
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
    )
    hot_water_consumption = models.DecimalField(
        _("Volume total - eau chaude"),
        validators=(MinValueValidator(Decimal("0")),),
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
    )
    # WATER
    water_consumption_charges = models.DecimalField(
        _("Consommation eau froide"),
        validators=(MinValueValidator(Decimal("0")),),
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
    )
    water_consumption = models.DecimalField(
        _("Volume total - eau froide"),
        validators=(MinValueValidator(Decimal("0")),),
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
    )
    # DJU
    dju_correction = models.PositiveSmallIntegerField(
        _("Correction DJU"), validators=(MinValueValidator(0),), null=True, blank=True
    )
