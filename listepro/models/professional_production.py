# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel

from .calculation_method import CalculationMethod
from .professional import Professional
from .usage_integrated import UsageIntegrated


class ProfessionalProduction(MixeurBaseModel):

    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)

    production_name = models.CharField(
        verbose_name=_("Nom de la réalisation"), max_length=256
    )
    place = models.CharField(verbose_name=_("Lieu de la réalisation"), max_length=256)
    label = models.CharField(
        verbose_name=_("Label de la réalisation"),
        max_length=256,
        blank=True,
    )
    year = models.IntegerField(verbose_name="Année de la la réalisation")
    consumption_before = models.IntegerField(
        verbose_name="Consomation avant travaux", blank=True, null=True
    )
    consumption_after = models.IntegerField(
        verbose_name="Consommation après travaux", blank=True, null=True
    )
    calculation_method = models.ForeignKey(
        CalculationMethod,
        verbose_name=("Méthode de calcul"),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    usage_integrated = models.ManyToManyField(
        UsageIntegrated,
        verbose_name=("Usages intégrés"),
    )
    history = models.CharField(verbose_name=_("Historique / contexte"), max_length=512)
    completed_mission = models.CharField(
        verbose_name=_("Missions réalisées"), max_length=512
    )
    thermal_envelope = models.CharField(
        verbose_name=_("Enveloppe thermique"),
        max_length=512,
        blank=True,
    )
    system = models.CharField(
        verbose_name=_("Système"),
        max_length=512,
        blank=True,
    )
    airtightness_test_result = models.CharField(
        verbose_name=_("Résultat du test d'étanchéité à l'air"),
        max_length=512,
        blank=True,
    )

    other_information = models.CharField(
        verbose_name=_("Autres informations sur ce projet"),
        max_length=512,
        blank=True,
    )
