# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import MixeurBaseModel


class Face(MixeurBaseModel):
    INSULATION_NATURE_OPTIONS = (
        ("synthetic", _("Synthétique")),
        ("mineral", _("Minéral")),
        ("biosourced", _("Biosourcé")),
        ("undetermined", _("Non déterminé")),
    )
    NATURE_OPTIONS = (
        ("wall", _("Mur")),
        ("floor", _("Sol")),
        ("roof", _("Toiture")),
        ("window", _("Fenêtre")),
    )

    class Meta:
        verbose_name = _("Paroi")

    report = models.ForeignKey(
        "visit_report.Report",
        verbose_name=_("Rapport"),
        on_delete=models.CASCADE,
        null=True,
        related_name="face",
    )

    evaluation = models.PositiveIntegerField(_("Evaluation"), default=2)

    comment = models.TextField(_("Commentaire"), blank=True, null=True)

    insulation_nature = models.CharField(
        _("Nature de l'isolant"),
        choices=INSULATION_NATURE_OPTIONS,
        max_length=20,
        blank=True,
        null=True,
    )

    nature = models.CharField(_("Type"), choices=NATURE_OPTIONS, max_length=20)

    data = models.CharField(_("Autres données"), max_length=2000, blank=True, null=True)
