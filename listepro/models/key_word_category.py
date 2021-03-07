# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel


class KeyWordCategory(MixeurBaseModel):

    order = models.IntegerField(verbose_name=_("Ordre d'affichage"), default=0)

    class Meta:
        verbose_name = _("Catégorie de mots-clé")
        verbose_name_plural = _("Catégories de mots-clé")
        ordering = ["order"]

    name = models.CharField(verbose_name=_("Catégorie de mots clés"), max_length=32)

    def __str__(self):
        return f"{self.order} - {self.name}"
