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


class AbstractCombustibleParams(MixeurBaseModel):
    class Meta:
        abstract = True

    COMBUSTIBLES = (
        (1, _("Fioul")),
        (2, _("Gaz de ville")),
        (3, _("Gaz propane")),
        (4, _("Réseau de chaleur")),
        (5, _("Électricité")),
        (6, _("Bois")),
    )

    combustible = models.PositiveSmallIntegerField(
        _("Combustible"), choices=COMBUSTIBLES
    )

    # ENERGY RATIO
    avg_hot_water_energy_ratio = models.DecimalField(
        _("Copro moy. - Ratio de consommation énergétique - eau chaude"),
        validators=(MinValueValidator(Decimal("0")),),
        max_digits=20,
        decimal_places=10,
    )
    eff_hot_water_energy_ratio = models.DecimalField(
        _("Copro perf. - Ratio de consommation énergétique - eau chaude"),
        validators=(MinValueValidator(Decimal("0")),),
        max_digits=20,
        decimal_places=10,
    )


class CombustibleParams(AbstractCombustibleParams):
    class Meta:
        verbose_name = _("Paramètres des combustibles")

    # COMBUSTIBLES
    params = models.ForeignKey(
        "autodiag_copro.Params",
        related_name="combustible_params",
        verbose_name=_("Paramètres"),
        on_delete=models.CASCADE,
    )


class DefaultCombustibleParams(AbstractCombustibleParams):
    class Meta:
        verbose_name = _("Paramètres des combustibles par défaut")

    # COMBUSTIBLES
    params = models.ForeignKey(
        "autodiag_copro.DefaultParams",
        related_name="combustible_params",
        verbose_name=_("Paramètres par défaut"),
        on_delete=models.CASCADE,
    )
