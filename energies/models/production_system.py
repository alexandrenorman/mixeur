from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from decimal import Decimal
from energies.models import Energy
from core.models import MixeurBaseModel


class ProductionSystem(MixeurBaseModel):
    class Meta:
        verbose_name = "Système de production d'énergie"

    SYSTEM_CHOICES = (
        ("oil_boiler_standard", "Chaudière fioul standard"),
        ("oil_boiler_condensing", "Chaudière fioul condensation"),
        ("gaz_boiler_standard", "Chaudière gaz standard"),
        ("gaz_boiler_condensing", "Chaudière gaz condensation"),
        ("propane_boiler_standard", "Chaudière propane standard"),
        ("propane_boiler_condensing", "Chaudière propane condensation"),
        ("electric_boiler", "Chaudière électrique"),
        ("electric_radiators", "Radiateurs électriques"),
        ("heat_pump_air_air", "PAC air/air"),
        ("heat_pump_air_water", "PAC air/eau "),
        (
            "heat_pump_geothermal_lte",
            "PAC géothermale avec émetteurs basse température",
        ),
        (
            "heat_pump_geothermal_vlte",
            "PAC géothermale avec émetteurs très basse température",
        ),
        ("thermodynamic_cmv", "VMC thermodynamique"),
        ("log_stove", "Poêle à bûches récent"),
        ("old_log_stove", "Poêle à bûches ancien"),
        ("log_insert", "Insert à bûches récent"),
        ("old_log_insert", "Insert à bûches ancien"),
        ("fireplace", "Cheminée ouverte"),
        ("granulated_wood_stove", "Poêle à bois granulés"),
        ("granulated_wood_boiler", "Chaudière à bois granulés"),
        ("log_boiler", "Chaudière à bûches"),
        ("shredded_wood_boiler", "Chaudière à bois déchiqueté"),
        ("recent_log_boiler_stove", "Poêle à bûches récent bouilleur"),
        ("granulated_wood_boiler_stove", "Poêle à bois granulés bouilleur"),
        ("electric_water_heater", "Chauffe-eau électrique"),
        ("ceti_outside_air", "CETI sur air extérieur"),
        ("ceti_inside_air", "CETI sur air intérieur"),
        ("ceti_extracted_air", "CETI sur air extrait"),
        (
            "heat_pump_using_waste_heat",
            "PAC valorisant une chaleur perdue (eaux grises etc.)",
        ),
        ("heating_network", "RCU (Réseau de Chaleur Urbain)"),
        ("solar_system_combined", "Système Solaire Combiné"),
        ("solar_water_heater", "Chauffe-eau Solaire"),
    )

    identifier = models.CharField(
        verbose_name="Identifiant", max_length=50, choices=SYSTEM_CHOICES, unique=True
    )
    energy = models.ForeignKey(
        Energy,
        verbose_name="Type d'énergie",
        on_delete=models.PROTECT,
        related_name="production_systems",
    )
    is_heating = models.BooleanField(verbose_name="Pour le chauffage ?", default=False)
    is_hot_water = models.BooleanField(
        verbose_name="Pour l'eau chaude ?", default=False
    )
    is_individual = models.BooleanField(
        verbose_name="Pour le logement individuel ?", default=False
    )
    is_multi_unit = models.BooleanField(
        verbose_name="Pour le logement collectif ?", default=False
    )
    is_hydro = models.BooleanField(
        verbose_name="Émission hydrolique centralisée ?", default=False
    )
    efficiency_heating = models.DecimalField(
        verbose_name="Rendement ou COP du chauffage",
        validators=(MinValueValidator(Decimal("0")),),
        blank=True,
        null=True,
        max_digits=4,
        decimal_places=2,
    )
    efficiency_hot_water = models.DecimalField(
        verbose_name="Rendement ou COP de l'eau chaude",
        validators=(MinValueValidator(Decimal("0")),),
        blank=True,
        null=True,
        max_digits=4,
        decimal_places=2,
    )
    enr_ratio_heating = models.DecimalField(
        verbose_name="Taux d'ENR du chauffage",
        validators=(MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("1"))),
        blank=True,
        null=True,
        max_digits=4,
        decimal_places=2,
    )
    enr_ratio_hot_water = models.DecimalField(
        verbose_name="Taux d'ENR de l'eau chaude",
        validators=(MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("1"))),
        blank=True,
        null=True,
        max_digits=4,
        decimal_places=2,
    )
    investment_individual_heating = models.IntegerField(
        verbose_name="Investissement pour le chauffage - logement individuel",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )
    investment_individual_hot_water = models.IntegerField(
        verbose_name="Investissement pour l'eau chaude - logement individuel",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )
    maintenance_individual_heating = models.IntegerField(
        verbose_name="Maintenance annuelle pour le chauffage - logement individuel",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )
    maintenance_individual_hot_water = models.IntegerField(
        verbose_name="Maintenance annuelle pour l'eau chaude' - logement individuel",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )
    investment_small_multi_unit_heating = models.IntegerField(
        verbose_name="Investissement pour le chauffage - logement collectif petit",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )
    investment_small_multi_unit_hot_water = models.IntegerField(
        verbose_name="Investissement pour l'eau chaude - logement collectif petit",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )
    maintenance_small_multi_unit_heating = models.IntegerField(
        verbose_name="Maintenance annuelle pour le chauffage - logement collectif petit",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )
    maintenance_small_multi_unit_hot_water = models.IntegerField(
        verbose_name="Maintenance annuelle pour l'eau chaude - logement collectif petit",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )
    provisions_small_multi_unit_heating = models.IntegerField(
        verbose_name="Provisions pour grosses réparations pour le chauffage - logement collectif petit",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )
    provisions_small_multi_unit_hot_water = models.IntegerField(
        verbose_name="Provisions pour grosses réparations pour l'eau chaude - logement collectif petit",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )
    investment_medium_multi_unit_heating = models.IntegerField(
        verbose_name="Investissement pour le chauffage - logement collectif moyen",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )
    investment_medium_multi_unit_hot_water = models.IntegerField(
        verbose_name="Investissement pour l'eau chaude - logement collectif moyen",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )
    maintenance_medium_multi_unit_heating = models.IntegerField(
        verbose_name="Maintenance annuelle pour le chauffage - logement collectif moyen",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )
    maintenance_medium_multi_unit_hot_water = models.IntegerField(
        verbose_name="Maintenance annuelle pour l'eau chaude - logement collectif moyen",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )
    provisions_medium_multi_unit_heating = models.IntegerField(
        verbose_name="Provisions pour grosses réparations pour le chauffage - logement collectif moyen",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )
    provisions_medium_multi_unit_hot_water = models.IntegerField(
        verbose_name="Provisions pour grosses réparations pour l'eau chaude - logement collectif moyen",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )
    investment_large_multi_unit_heating = models.IntegerField(
        verbose_name="Investissement pour le chauffage - logement collectif grand",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )
    investment_large_multi_unit_hot_water = models.IntegerField(
        verbose_name="Investissement pour l'eau chaude - logement collectif grand",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )
    maintenance_large_multi_unit_heating = models.IntegerField(
        verbose_name="Maintenance annuelle pour le chauffage - logement collectif grand",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )
    maintenance_large_multi_unit_hot_water = models.IntegerField(
        verbose_name="Maintenance annuelle pour l'eau chaude - logement collectif grand",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )
    provisions_large_multi_unit_heating = models.IntegerField(
        verbose_name="Provisions pour grosses réparations pour le chauffage - logement collectif grand",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )
    provisions_large_multi_unit_hot_water = models.IntegerField(
        verbose_name="Provisions pour grosses réparations pour l'eau chaude - logement collectif grand",
        validators=(MinValueValidator(0),),
        blank=True,
        null=True,
    )

    @property
    def name(self):
        return self.get_identifier_display()

    @property
    def is_thermal_solar(self):
        return self.identifier in ("solar_system_combined", "solar_water_heater")

    @property
    def is_heat_pump(self):
        return self.identifier in (
            "heat_pump_air_air",
            "heat_pump_air_water",
            "heat_pump_geothermal_lte",
            "heat_pump_geothermal_vlte",
            "thermodynamic_cmv",
        )

    @staticmethod
    def get_heat_pump_enr_ratio(efficiency):
        if not efficiency:
            return None
        ratio = Decimal("1") - Decimal("2.58") / efficiency
        return ratio.quantize(Decimal("0.01")) if ratio > Decimal("0") else Decimal("0")

    def __str__(self):
        return self.name

    def clean(self):
        # Force properties to None according to boolean fields
        if not self.is_heating:
            self.efficiency_heating = None
            self.enr_ratio_heating = None
            self.investment_individual_heating = None
            self.maintenance_individual_heating = None
            self.investment_small_multi_unit_heating = None
            self.maintenance_small_multi_unit_heating = None
            self.provisions_small_multi_unit_heating = None
            self.investment_medium_multi_unit_heating = None
            self.maintenance_medium_multi_unit_heating = None
            self.provisions_medium_multi_unit_heating = None
            self.investment_large_multi_unit_heating = None
            self.maintenance_large_multi_unit_heating = None
            self.provisions_large_multi_unit_heating = None
        if not self.is_hot_water:
            self.efficiency_hot_water = None
            self.enr_ratio_hot_water = None
            self.investment_individual_hot_water = None
            self.maintenance_individual_hot_water = None
            self.investment_small_multi_unit_hot_water = None
            self.maintenance_small_multi_unit_hot_water = None
            self.provisions_small_multi_unit_hot_water = None
            self.investment_medium_multi_unit_hot_water = None
            self.maintenance_medium_multi_unit_hot_water = None
            self.provisions_medium_multi_unit_hot_water = None
            self.investment_large_multi_unit_hot_water = None
            self.maintenance_large_multi_unit_hot_water = None
            self.provisions_large_multi_unit_hot_water = None
        if not self.is_individual:
            self.investment_individual_heating = None
            self.investment_individual_hot_water = None
            self.maintenance_individual_heating = None
            self.maintenance_individual_hot_water = None
        if not self.is_multi_unit:
            self.investment_small_multi_unit_heating = None
            self.investment_small_multi_unit_hot_water = None
            self.maintenance_small_multi_unit_heating = None
            self.maintenance_small_multi_unit_hot_water = None
            self.provisions_small_multi_unit_heating = None
            self.provisions_small_multi_unit_hot_water = None
            self.investment_medium_multi_unit_heating = None
            self.investment_medium_multi_unit_hot_water = None
            self.maintenance_medium_multi_unit_heating = None
            self.maintenance_medium_multi_unit_hot_water = None
            self.provisions_medium_multi_unit_heating = None
            self.provisions_medium_multi_unit_hot_water = None
            self.investment_large_multi_unit_heating = None
            self.investment_large_multi_unit_hot_water = None
            self.maintenance_large_multi_unit_heating = None
            self.maintenance_large_multi_unit_hot_water = None
            self.provisions_large_multi_unit_heating = None
            self.provisions_large_multi_unit_hot_water = None
