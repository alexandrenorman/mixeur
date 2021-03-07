# -*- coding: utf-8 -*-
from decimal import Decimal
from django.db import models
from helpers.mixins import UniversalReprMixin, StoreDataWithDefaultValueByKey
from core.models import MixeurBaseModel
from django.utils.translation import ugettext_lazy as _

from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


# leaves function to not break migrations
def validation_absolute_positive(value):
    if value < 1:
        raise ValidationError(f"Value must be > 1 (was {value}")


class AbstractParams(models.Model, UniversalReprMixin):
    class Meta:
        abstract = True

    avg_living_area = models.PositiveSmallIntegerField(
        _("Surface moyenne d'un logement"),
        validators=(MinValueValidator(0),),
        default=1,
    )
    # AVERAGE
    avg_hot_water_conso_ratio = models.DecimalField(
        _("Copro moy. - Ratio de consommation - eau chaude"),
        validators=(MinValueValidator(Decimal("0")),),
        max_digits=20,
        decimal_places=10,
    )
    avg_water_conso_ratio = models.DecimalField(
        _("Copro moy. - Ratio de consommation - eau froide"),
        validators=(MinValueValidator(Decimal("0")),),
        max_digits=20,
        decimal_places=10,
    )
    # EFFICIENT
    eff_hot_water_conso_ratio = models.DecimalField(
        _("Copro perf. - Ratio de consommation - eau chaude"),
        validators=(MinValueValidator(Decimal("0")),),
        max_digits=20,
        decimal_places=10,
    )
    eff_water_conso_ratio = models.DecimalField(
        _("Copro perf. - Ratio de consommation - eau froide"),
        validators=(MinValueValidator(Decimal("0")),),
        max_digits=20,
        decimal_places=10,
    )


class Params(AbstractParams, MixeurBaseModel):
    class Meta:
        verbose_name = _("Paramètres")


class DefaultParams(AbstractParams, StoreDataWithDefaultValueByKey):
    class Meta:
        verbose_name = _("Paramètres par défault")

    key = models.ForeignKey(
        "accounts.group",
        verbose_name=_("Structure"),
        on_delete=models.CASCADE,
        null=True,
    )
