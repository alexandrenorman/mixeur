# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel

from .key_word_category import KeyWordCategory


class KeyWord(MixeurBaseModel):

    order = models.IntegerField(verbose_name=_("Ordre d'affichage"), default=0)

    class Meta:
        verbose_name = _("Mot-clé")
        verbose_name_plural = _("Mots-clé")
        ordering = ["order"]

    name = models.CharField(verbose_name=_("Mot clé"), max_length=32)
    category = models.ForeignKey(
        KeyWordCategory,
        verbose_name="Catégorie du mot-clé",
        related_name="key_words",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.order} - {self.name}"
