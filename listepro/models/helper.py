# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel


class Helper(MixeurBaseModel):
    class Meta:
        verbose_name = _("Aide")
        verbose_name_plural = _("Aides")

    name = models.CharField(
        max_length=128,
    )
    help_text = models.TextField(
        verbose_name=_("Texte de l'aide"),
        blank=True,
    )

    def __str__(self):
        return self.name
