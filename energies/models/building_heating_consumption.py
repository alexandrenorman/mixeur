from django.core.validators import MinValueValidator
from django.db import models

from core.models import MixeurBaseModel


class BuildingHeatingConsumption(MixeurBaseModel):

    CRITERION_CHOICES = (
        ("before_1919", "Avant 1919"),  # 170
        ("between_1919_1945", "Entre 1919 et 1945"),  # 190
        ("between_1946_1970", "Entre 1946 et 1970"),  # 170
        ("between_1971_1990", "Entre 1971 et 1990"),  # 136
        ("between_1991_2005", "Entre 1991 et 2005"),  # 117
        ("between_2006_2012", "Entre 2006 et 2012"),  # 94
        ("after_2012", "Après 2012"),  # 32
        ("bbc", "Bâtiment rénové au niveau basse consommation (BBC)"),  # 60
        ("passive", "Bâtiment rénové au niveau passif"),  # 15
    )

    # CRITERION_CHOICES = (
    #     ("before_1948", "Avant 1948"),
    #     ("between_1948_1974", "Entre 1948 et 1974"),
    #     ("between_1975_1982", "Entre 1975 et 1982"),
    #     ("between_1983_1988", "Entre 1983 et 1988"),
    #     ("between_1989_2000", "Entre 1989 et 2000"),
    #     ("between_2001_2005", "Entre 2001 et 2005"),
    #     ("between_2006_2012", "Entre 2006 et 2012"),
    #     ("after_2012", "Après 2012"),
    #     ("bbc", "Bâtiment BBC"),
    #     ("passive", "Bâtiment passif"),
    # )

    class Meta:
        verbose_name = "Consommation en chauffage"

    criterion = models.CharField(
        max_length=30, verbose_name="Critère", unique=True, choices=CRITERION_CHOICES
    )
    heating_consumption = models.IntegerField(
        validators=(MinValueValidator(1),),
        verbose_name="Consommation de chauffage en kWh/m²",
    )
    comment = models.CharField(
        max_length=50, blank=True, default="", verbose_name="Commentaire"
    )
    order = models.IntegerField(
        default=0, verbose_name="Ordre d'affichage", db_index=True
    )

    @property
    def name(self):
        return self.get_criterion_display()
