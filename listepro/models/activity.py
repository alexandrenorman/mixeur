# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel

ACTIVITY_ICON_CHOICES = (
    ("icon-collectif", _("Icône petit collectif")),
    ("icon-copro", _("Icône copropriété")),
    ("icon-maison", _("Icône Maison")),
    ("icon-tertiaire", _("Icône tertiaire")),
    ("icon-help", _("Icône par defaut")),
)


class Activity(MixeurBaseModel):

    order = models.IntegerField(verbose_name=_("Ordre d'affichage"), default=0)

    class Meta:
        verbose_name = _("Activité")
        verbose_name_plural = _("Activités")
        ordering = ["order"]

    name = models.CharField(verbose_name=_("Activités"), max_length=32)
    icon = models.CharField(
        verbose_name=_("Icônes"),
        default="icon-help",
        choices=ACTIVITY_ICON_CHOICES,
        max_length=32,
    )

    def __str__(self):
        return f"{self.order} - {self.name}"
