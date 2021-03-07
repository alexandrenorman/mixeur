# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import MixeurBaseModel


class Appendix(MixeurBaseModel):
    class Meta:
        verbose_name = _("Annexe")

    report = models.ForeignKey(
        "visit_report.Report",
        verbose_name=_("Rapport"),
        on_delete=models.CASCADE,
        related_name="appendix",
    )

    name = models.CharField(_("Nom"), max_length=50, blank=True, null=True)

    # TO: ELX: S'il existe, c'est qu'on en veut, non ?
    selected = models.BooleanField(_("Sélectionné"), default=False)
