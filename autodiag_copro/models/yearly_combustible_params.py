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


class AbstractYearlyCombustibleParams(MixeurBaseModel):
    class Meta:
        abstract = True

    years = models.CharField(_("Années"), max_length=9)

    # COST RATIO
    avg_energy_cost_ratio = models.DecimalField(
        _("Copro moy. - Ratio de coût énergie"),
        validators=(MinValueValidator(Decimal("0")),),
        max_digits=20,
        decimal_places=10,
    )
    eff_energy_cost_ratio = models.DecimalField(
        _("Copro perf. - Ratio de coût énergie"),
        validators=(MinValueValidator(Decimal("0")),),
        max_digits=20,
        decimal_places=10,
    )


class YearlyCombustibleParams(AbstractYearlyCombustibleParams):
    class Meta:
        verbose_name = _("Paramètres annuels des combustibles")
        unique_together = ("combustible_params", "years")

    # COMBUSTIBLES
    combustible_params = models.ForeignKey(
        "autodiag_copro.CombustibleParams",
        related_name="yearly_combustible_params",
        verbose_name=_("Paramètres de combustible"),
        on_delete=models.CASCADE,
    )


class DefaultYearlyCombustibleParams(AbstractYearlyCombustibleParams):
    class Meta:
        verbose_name = _("Paramètres annuels des combustibles par défaut")
        unique_together = ("combustible_params", "years")

    # COMBUSTIBLES
    combustible_params = models.ForeignKey(
        "autodiag_copro.DefaultCombustibleParams",
        related_name="yearly_combustible_params",
        verbose_name=_("Paramètres de combustible par défaut"),
        on_delete=models.CASCADE,
    )
