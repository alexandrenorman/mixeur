# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import MixeurBaseModel


class ScenarioSummary(MixeurBaseModel):
    class Meta:
        verbose_name = _("Résumé du scénario")
        verbose_name_plural = _("Résumés des scénarii")

    scenario = models.ForeignKey(
        "visit_report.Scenario", verbose_name=_("Scénario"), on_delete=models.CASCADE
    )

    nature = models.CharField(_("Type"), max_length=50, blank=True, null=True)

    # TO: ELX: S'il existe, c'est qu'on en veut, non ?
    selected = models.BooleanField(_("Sélectionné"), default=False)
