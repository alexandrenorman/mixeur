# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import MixeurBaseModel


class FinancialAid(MixeurBaseModel):
    class Meta:
        verbose_name = _("Aide financière")
        verbose_name_plural = _("Aides financières")

    scenario = models.ForeignKey(
        "visit_report.Scenario", verbose_name=_("Scénario"), on_delete=models.CASCADE
    )

    amount = models.PositiveIntegerField(_("Montant"), default=0)

    selected = models.BooleanField(_("Sélectionnée"), default=False)

    custom_label = models.CharField(
        _("Label personnalisé"), max_length=200, blank=True, null=True
    )

    nature = models.CharField(_("Type"), max_length=50, blank=True, null=True)
