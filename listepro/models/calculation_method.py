# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel


class CalculationMethod(MixeurBaseModel):

    order = models.IntegerField(verbose_name=_("Ordre d'affichage"), default=0)

    class Meta:
        verbose_name = _("Méthode de calcul")
        verbose_name_plural = _("Méthodes de calcul")
        ordering = ["order"]

    name = models.CharField(verbose_name=_("Méthodes de calcul"), max_length=128)

    def __str__(self):
        return f"{self.order} - {self.name}"
