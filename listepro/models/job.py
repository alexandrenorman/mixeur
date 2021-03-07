# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel


class Job(MixeurBaseModel):

    order = models.IntegerField(verbose_name=_("Ordre d'affichage"), default=0)

    class Meta:
        verbose_name = _("Métier")
        verbose_name_plural = _("Métiers")
        ordering = ["order"]

    name = models.CharField(verbose_name=_("Métiers"), max_length=32)

    def __str__(self):
        return f"{self.order} - {self.name}"
