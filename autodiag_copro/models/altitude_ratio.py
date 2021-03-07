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


class AltitudeRatio(MixeurBaseModel):
    class Meta:
        verbose_name = _("Indice d'altitude")

    altitude = models.CharField(_("Altitude"), max_length=300)
    value = models.DecimalField(
        _("Indice"),
        validators=(MinValueValidator(Decimal("0")),),
        max_digits=20,
        decimal_places=2,
    )
