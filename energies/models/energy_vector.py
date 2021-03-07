from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from energies.models import Energy
from core.models import MixeurBaseModel


class EnergyVector(MixeurBaseModel):

    VECTOR_CHOICES = (
        ("oil_kg", "fioul acheté au kg"),
        ("oil_l", "fioul acheté au litre"),
        ("oil_kwh", "fioul au kWh"),
        ("propane_kg", "propane acheté au kg"),
        ("propane_m3", "Propane acheté au m³"),
        ("propane_bottles", "propane acheté en bouteilles de 13 kg"),
        ("propane_kwh", "propane en kWh"),
        ("natural_gaz_m3", "gaz naturel au m3"),
        ("natural_gaz_kwh", "gaz naturel au kWh"),
        ("electricity_kwh", "Electricité"),
        ("rcu_kwh", "RCU (réseau de chaleur urbain)"),
        ("wood_logs_stere", "bûches"),
        ("granules_t", "granulés en vrac"),
        ("granules_bag", "granulés en sac"),
        ("shredded_wood_t", "bois déchiqueté à la tonne"),
        ("shredded_wood_map", "bois déchiqueté au MAP"),
        ("shredded_wood_kwh", "bois déchiqueté au kWh"),
    )

    class Meta:
        verbose_name = "Vecteurs d'énergie"

    vector = models.CharField(
        max_length=30,
        unique=True,
        choices=VECTOR_CHOICES,
        verbose_name="Vecteur énergétique",
    )

    buying_unit = models.CharField(max_length=200, verbose_name="Unité d'achat")

    pci = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        default=0,
        verbose_name="Pouvoir calorifique inférieur en kWh/unité",
        validators=(MinValueValidator(Decimal("0")),),
    )

    unit = models.CharField(max_length=200, verbose_name="Unité")

    energy = models.ForeignKey(
        Energy,
        verbose_name="Type d'énergie",
        on_delete=models.PROTECT,
        related_name="vectors",
    )

    order = models.IntegerField(
        default=0, verbose_name="Ordre d'affichage", db_index=True
    )
