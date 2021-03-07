# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel

from .mission import Mission


class SubMission(MixeurBaseModel):

    order = models.IntegerField(verbose_name=_("Ordre d'affichage"), default=0)

    class Meta:
        verbose_name = _("Sous mission")
        verbose_name_plural = _("Sous missions")
        ordering = ["mission__order", "order"]

    mission = models.ForeignKey(
        Mission,
        verbose_name=_("Groupe de mission"),
        on_delete=models.CASCADE,
        related_name="sub_missions",
    )

    name = models.CharField(
        verbose_name=_("Missions proposés"),
        help_text=_(
            "Sélectionnez les missions que vous proposez pour lesquelles vous avez fourni\
                 des références auprès de l'espace info énergie"
        ),
        max_length=128,
    )

    help_text = models.TextField(
        verbose_name=_("Texte de l'aide"),
        blank=True,
    )

    def __str__(self):
        return f"{self.name} ({self.mission.name})"
