# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import MixeurBaseModel


class Scenario(MixeurBaseModel):
    NATURE_OPTIONS = (
        ("primary", _("Scénario principal")),
        ("secondary", _("Scénario secondaire")),
    )

    class Meta:
        verbose_name = _("Scénario")

    report = models.ForeignKey(
        "visit_report.Report",
        verbose_name=_("Rapport"),
        on_delete=models.CASCADE,
        null=True,
        related_name="scenario",
    )

    nature = models.CharField(_("Type"), choices=NATURE_OPTIONS, max_length=20)

    label = models.CharField(_("Label"), max_length=50, blank=False, null=False)

    custom_summary = models.TextField(_("Résumé personnalisé"), blank=True, null=True)

    is_custom_summary_selected = models.BooleanField(
        _("Résumé personnalisé sélectionné"), default=False
    )
