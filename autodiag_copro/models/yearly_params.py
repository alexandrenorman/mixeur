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


class AbstractYearlyParams(MixeurBaseModel):
    class Meta:
        abstract = True

    years = models.CharField(_("Années"), max_length=9)

    water_cost = models.DecimalField(
        _("Prix eau froide"),
        validators=(MinValueValidator(Decimal("0")),),
        max_digits=20,
        decimal_places=10,
    )


class YearlyParams(AbstractYearlyParams):
    class Meta:
        verbose_name = _("Paramètres annuels")
        unique_together = ("params", "years")

    # PARAMS
    params = models.ForeignKey(
        "autodiag_copro.Params",
        related_name="yearly_params",
        verbose_name=_("Paramètres"),
        on_delete=models.CASCADE,
    )


class DefaultYearlyParams(AbstractYearlyParams):
    class Meta:
        verbose_name = _("Paramètres annuels par défault")
        unique_together = ("params", "years")

    # PARAMS
    params = models.ForeignKey(
        "autodiag_copro.DefaultParams",
        related_name="yearly_params",
        verbose_name=_("Paramètres par défaut"),
        on_delete=models.CASCADE,
    )
