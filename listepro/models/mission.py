# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel


class Mission(MixeurBaseModel):

    order = models.IntegerField(verbose_name=_("Ordre d'affichage"), default=0)

    class Meta:
        verbose_name = _("Mission")
        verbose_name_plural = _("Missions")
        ordering = ["order"]

    name = models.CharField(verbose_name=_("Groupes de missions"), max_length=128)
    help_text = models.TextField(
        verbose_name=_("Texte de l'aide"),
        blank=True,
    )

    def __str__(self):
        return f"{self.order} - {self.name}"
