# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel


class UsageIntegrated(MixeurBaseModel):

    order = models.IntegerField(verbose_name=_("Ordre d'affichage"), default=0)

    class Meta:
        verbose_name = _("Usage intégré")
        verbose_name_plural = _("Usages intégrés")
        ordering = ["order"]

    name = models.CharField(
        verbose_name=_("Usages intégrés dans le calcul"), max_length=128,
    )

    def __str__(self):
        return f"{self.order} - {self.name}"
