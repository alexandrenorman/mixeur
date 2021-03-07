# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import MixeurBaseModel


class System(MixeurBaseModel):
    NATURE_OPTIONS = (
        ("heating-main", _("Production de chauffage")),
        ("emitter", _("Emetteur")),
        ("controler", _("Régulation")),
        ("hot-water", _("Production d'eau chaude")),
        ("heating-extra", _("Chauffage d'appoint")),
        ("ventilation", _("Ventilation")),
        ("photovoltaic", _("Photovoltaïque")),
    )

    class Meta:
        verbose_name = _("Système")

    report = models.ForeignKey(
        "visit_report.Report",
        verbose_name=_("Rapport"),
        on_delete=models.CASCADE,
        null=True,
        related_name="system",
    )

    nature = models.CharField(_("Type"), choices=NATURE_OPTIONS, max_length=20)

    data = models.TextField(_("Autres données"), blank=True, null=True)
