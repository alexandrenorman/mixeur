# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel

SEGMENT_ICON_CHOICES = (
    ("icon-renovation", _("Icône rénovation")),
    ("icon-neuve", _("Icône neuve")),
    ("icon-help", _("Icône par defaut")),
)


class Segment(MixeurBaseModel):

    order = models.IntegerField(verbose_name=_("Ordre d'affichage"), default=0)

    class Meta:
        verbose_name = _("Segment de marché")
        verbose_name_plural = _("Segments de marché")
        ordering = ["order"]

    name = models.CharField(verbose_name=_("Segment"), max_length=32)

    icon = models.CharField(
        verbose_name=_("Icônes"),
        default="icon-help",
        choices=SEGMENT_ICON_CHOICES,
        max_length=32,
    )

    def __str__(self):
        return f"{self.order} - {self.name}"

    def get_html_id(self):
        return f"segment-{self.id}"
