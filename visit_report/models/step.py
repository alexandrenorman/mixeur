# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import MixeurBaseModel


class Step(MixeurBaseModel):
    CATEGORY_OPTIONS = (
        ("financing", _("Quand demander les aides financières ?")),
        ("contacts", _("Qui contacter ?")),
    )
    MILESTONE_OPTIONS = (
        ("advises", _("Conseils/Programmation")),
        ("estimation", _("Réalisation du devis")),
        ("estimation-signature", _("Signature du devis")),
        ("work-beginning", _("Début des travaux")),
        ("work-end", _("Fin des travaux")),
    )
    STEP_TYPE_OPTIONS = (
        ("simple", _("Simple")),
        ("info", _("Avec infos supplémentaires")),
        ("contact", _("Avec coordonnées de contact")),
        ("field", _("Avec saisie libre")),
    )

    class Meta:
        verbose_name = _("Etape")

    report = models.ForeignKey(
        "visit_report.Report",
        verbose_name=_("Rapport"),
        on_delete=models.CASCADE,
        null=True,
        related_name="step",
    )

    category = models.CharField(
        _("Catégorie"), choices=CATEGORY_OPTIONS, max_length=25, blank=True, null=True
    )

    milestone = models.CharField(
        _("Etape du projet"),
        choices=MILESTONE_OPTIONS,
        max_length=25,
        blank=True,
        null=True,
    )

    order = models.PositiveIntegerField(_("Ordre"), default=0)

    step_type = models.CharField(
        _("Type"), choices=STEP_TYPE_OPTIONS, default="regular", max_length=25
    )

    nature = models.CharField(_("Type"), max_length=50, blank=True, null=True)

    data = models.TextField(_("Autres données"), blank=True, null=True)

    # TO: ELX: S'il existe, c'est qu'on en veut, non ?
    selected = models.BooleanField(_("Sélectionné"), default=False)
