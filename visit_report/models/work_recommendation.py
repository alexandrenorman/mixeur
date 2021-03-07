# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import MixeurBaseModel

# from django.core.exceptions import ValidationError


class WorkRecommendation(MixeurBaseModel):
    CATEGORY_OPTIONS = (
        ("enveloppe", _("Enveloppe")),
        ("systems", _("Système")),
        ("others", _("Autres")),
        ("eco-gestures", _("Eco gestes")),
    )
    NATURE_OPTIONS = (
        ("roof-insulation", _("Isolation de la toiture")),
        ("wall-insulation", _("Isolation des murs")),
        ("floor-insulation", _("Isolation du plancher bas")),
        ("carpentry-replacement", _("Remplacement des menuiseries")),
        ("ventilation", _("VMC")),
        ("heating-production", _("Production de chaleur")),
        ("heating-emitter", _("Production de chaleur")),
        ("hot-water-production", _("Production d'eau chaude sanitaire")),
        ("heating-control", _("Régulation du système de chauffage")),
        ("photovoltaic", _("Installation de panneaux solaires photovoltaïques")),
        ("eco-gestures", _("Eco gestes")),
        ("calorifuge", _("Calorifuge")),
        ("water-tank-insulation", _("water-tank-insulation")),
        ("additional-costs", _("Frais supplémentaires")),
    )

    class Meta:
        verbose_name = _("Recommendation de travaux")
        verbose_name_plural = _("Recommendations de travaux")

    report = models.ForeignKey(
        "visit_report.Report",
        verbose_name=_("Rapport"),
        on_delete=models.CASCADE,
        null=True,
        related_name="work_recommendation",
    )

    category = models.CharField(_("Catégorie"), choices=CATEGORY_OPTIONS, max_length=25)

    nature = models.CharField(_("Type"), choices=NATURE_OPTIONS, max_length=50)

    # Comment gérer le fait que chaque type ait sa propre liste de noms possibles ?
    # TO:ELX: ça va se gérer dans l'UI pour l'affichage / sélection
    # et dans la méthode clean du model pour valider
    # que les choix faits sont cohérents
    # -> voir en dessous la méthode commenté
    name = models.CharField(_("Nom"), max_length=50, blank=True, null=True)

    selected = models.BooleanField(_("Sélectionné"), default=False)

    cost = models.PositiveIntegerField(_("Coût estimé"), default=0)

    comment = models.TextField(_("Commentaires"), blank=True, null=True)

    selected_scenario_primary = models.BooleanField(
        _("Sélectionné dans le scénario principal"), default=False
    )

    selected_scenario_secondary = models.BooleanField(
        _("Sélectionné dans le scénario secondaire"), default=False
    )

    data = models.TextField(_("Autres données"), blank=True, null=True)

    # def clean(self):
    #     check_list = {
    #         "roof_insulation": ["laine de verre", "purée"],
    #         "wall_insulation": [],
    #         "floor_insulation": [],
    #         "carpentry_replacement": [],
    #         "ventilation": [],
    #         "heating_production": [],
    #         "hot_water_production": [],
    #         "heating_control": [],
    #         "photovoltaic": [],
    #         "eco_gestures": [],
    #     }
    #     if self.name not in check_list[self.nature]:
    #         raise ValidationError(
    #             _(
    #                 "Le nom ne correspond pas au type choisi"
    #             )
    #         )
