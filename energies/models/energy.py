# -*- coding: utf-8 -*-
import statistics
from decimal import Decimal
from operator import attrgetter

from django.core.validators import MinValueValidator
from django.db import models

from core.models import MixeurBaseModel


class Energy(MixeurBaseModel):
    class Meta:
        verbose_name = "Énergie"

    ENERGIE_CHOICES = (
        ("oil", "Fioul"),
        ("gaz_b0", "Gaz B0"),
        ("gaz_b1", "Gaz B1"),
        ("propane", "Propane"),
        ("electricity", "Électricité"),
        ("wood", "Bois"),
        ("shredded_wood", "Bois déchiqueté"),
        ("bulk_granules", "Bois granulés en vrac"),
        ("bag_granules", "Bois granulés en sac"),
        ("network", "Réseau"),
        ("thermal_solar", "Solaire thermique"),
    )

    COMBUSTIBLE_CATEGORY_CHOICES = (
        ("fossil", "Fossile"),
        ("electricity", "Électricité"),
        ("renewable", "Renouvelable"),
    )

    identifier = models.CharField(
        verbose_name="Identifiant d'énergie",
        max_length=30,
        choices=ENERGIE_CHOICES,
        unique=True,
    )

    primary_energy_ratio = models.DecimalField(
        verbose_name="Ratio d'énergie primaire",
        validators=(MinValueValidator(Decimal("1")),),
        max_digits=20,
        decimal_places=10,
    )
    ghg_ratio = models.DecimalField(
        verbose_name="Ratio gaz à effet de serre",
        validators=(MinValueValidator(Decimal("1")),),
        max_digits=20,
        decimal_places=10,
    )
    carbon_tax = models.BooleanField(
        verbose_name="Assujeti à la taxe carbone ?", default=False
    )
    pci_ratio = models.PositiveSmallIntegerField(
        verbose_name="Ratio de pouvoir calorifique inférieur",
        validators=(MinValueValidator(Decimal("1")),),
        null=True,
    )
    density_ratio = models.DecimalField(
        verbose_name="Ratio de densité",
        validators=(MinValueValidator(Decimal("1")),),
        max_digits=20,
        decimal_places=10,
        null=True,
    )
    combustible_category = models.CharField(
        verbose_name="Catégorie de combustible",
        max_length=30,
        choices=COMBUSTIBLE_CATEGORY_CHOICES,
        default="fossil",
    )
    price_variation = models.DecimalField(
        verbose_name="Variation du prix depuis 2002", max_digits=6, decimal_places=5
    )
    price_multi_unit_discount = models.DecimalField(
        verbose_name="Ratio appliqué sur le prix pour logement collectifs",
        max_digits=3,
        decimal_places=2,
        default=Decimal("0.85"),
    )

    def __str__(self):
        return self.name

    @property
    def current_price(self):
        """
        Return price of the current year
        Looping on yearly_energy_price.all() allow to use prefetch_related and avoid an extra db query by Energy
        """
        yearly_prices = list(self.yearly_energy_price.all())
        if not yearly_prices:
            return None
        three_last_yearly_prices = sorted(yearly_prices, key=attrgetter("year"))[-3:]
        prices = [yp.price for yp in three_last_yearly_prices if yp.price]
        if not prices:
            return None
        return statistics.mean(prices).quantize(Decimal("0.01"))

    @property
    def current_price_multi_unit(self):
        """
        Return price of the current year with multi unit discout applied
        """
        if self.current_price is None:
            return None
        current_price_multi_unit = self.current_price * self.price_multi_unit_discount
        return current_price_multi_unit.quantize(Decimal("0.01"))

    @property
    def name(self):
        return self.get_identifier_display()
