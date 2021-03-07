# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel


class Explanation(MixeurBaseModel):
    class Meta:
        verbose_name = _("Explications")
        verbose_name_plural = _("Explications")
        constraints = [
            models.UniqueConstraint(
                fields=["owning_group"], name="one_explanation_by_group"
            )
        ]
        # ordering = ["-date"]

    owning_group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe propriétaire"),
        on_delete=models.CASCADE,
        null=False,
        related_name="experiences_explanation",
    )

    starting_a_project = models.TextField(
        verbose_name=_("Lancer un projet"), blank=True, null=True
    )
    usefull_docs = models.TextField(
        verbose_name=_("Documents utiles"), blank=True, null=True
    )
