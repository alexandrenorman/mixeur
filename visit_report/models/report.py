# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import MixeurBaseModel
import django.utils.timezone


class Report(MixeurBaseModel):
    INFORMATION_SOURCE_OPTIONS = (
        ("bill", _("Facture")),
        ("dpe", _("DPE")),
        ("declarative", _("Déclaratif")),
        ("estimative", _("Estimatif")),
        ("unavailable", _("Non disponible")),
    )
    DPE_OPTIONS = (
        ("a", _("Classe A")),
        ("b", _("Classe B")),
        ("c", _("Classe C")),
        ("d", _("Classe D")),
        ("e", _("Classe E")),
        ("-", _("Non connu")),
    )

    class Meta:
        verbose_name = _("Rapport de visite")
        verbose_name_plural = _("Rapports de visite")

    housing = models.OneToOneField(
        "housing",
        verbose_name=_("Logement associé"),
        on_delete=models.CASCADE,
        null=True,
        related_name="report",
    )

    advisor = models.ForeignKey(
        "accounts.User",
        verbose_name=_("Conseiller"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="report",
        limit_choices_to=models.Q(user_type="advisor")
        | models.Q(user_type="superadvisor"),
    )

    group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Structure signataire"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="report",
        limit_choices_to={"is_admin": False},
    )

    fiscal_income = models.DecimalField(
        _("Revenu fiscal de référence"),
        default=0,
        blank=True,
        null=True,
        max_digits=8,
        decimal_places=2,
    )

    consumption_information_source = models.CharField(
        _("Source d'information"),
        choices=INFORMATION_SOURCE_OPTIONS,
        max_length=30,
        blank=True,
        null=True,
    )

    consumption_heating = models.PositiveIntegerField(_("Chauffage"), default=0)

    consumption_hot_water = models.PositiveIntegerField(
        _("Eau chaude sanitaire"), default=0, blank=True
    )

    consumption_heating_hot_water = models.PositiveIntegerField(
        _("Chauffage et eau chaude groupés"), default=0, blank=True
    )

    consumption_electricity = models.PositiveIntegerField(
        _("Electricité hors chauffage"), default=0
    )

    dpe = models.CharField(
        _("DPE"), choices=DPE_OPTIONS, max_length=2, default="-", blank=True
    )

    is_secondary_scenario_displayed = models.BooleanField(
        _("Afficher le scénario secondaire"), default=True
    )

    is_custom_appendix_selected = models.BooleanField(
        _("Annexe personnalisée sélectionné"), default=False
    )

    custom_appendix = models.TextField(_("Annexe personnalisée"), blank=True, null=True)

    identity_comment = models.TextField(
        _("Commentaire sur l'identité du maître d'ouvrage"), blank=True, null=True
    )

    housing_comment = models.TextField(
        _("Commentaire sur l'identité du logement"), blank=True, null=True
    )

    consumption_comment = models.TextField(
        _("Commentaire sur consommations d'énergie"), blank=True, null=True
    )

    house_inventory_comment = models.TextField(
        _("Commentaire sur l'état des lieux du logement"), blank=True, null=True
    )
    work_recommendations_comment = models.TextField(
        _("Commentaire sur les recommandations de travaux"), blank=True, null=True
    )
    financing_comment = models.TextField(
        _("Commentaire sur le financement du projet"), blank=True, null=True
    )
    conclusion_comment = models.TextField(
        _("Commentaire sur la conclusion du rapport"), blank=True, null=True
    )

    visit_date = models.DateField(
        _("Date de la visite"), default=django.utils.timezone.now
    )
