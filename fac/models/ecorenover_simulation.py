# -*- coding: utf-8 -*-
from django.contrib.postgres.fields import JSONField

from core.models import MixeurBaseModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class EcorenoverQueryset(models.QuerySet):
    def accessible_by(self, user):
        if user.is_administrator:
            return self

        return self.filter(owning_group=user.group)


class EcorenoverManager(models.Manager.from_queryset(EcorenoverQueryset)):
    def get_queryset(self):
        return super().get_queryset()


class EcorenoverSimulation(MixeurBaseModel):
    """
    Saved Ecorenover simulation
    """

    objects = EcorenoverManager()

    class Meta:
        verbose_name = _("Simulation écorenover")
        verbose_name_plural = _("Simulations écorenover")
        ordering = ("-updated_at",)

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    # linked organization or contact (and maybe other models later on)
    linked_object = GenericForeignKey("content_type", "object_id")

    description = models.TextField(
        verbose_name=_("Description"), default="", blank=True
    )
    saved_inputs = JSONField(verbose_name=_("Données sauvegardées"), default=dict)
    owning_group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe propriétaire"),
        on_delete=models.CASCADE,
        null=False,
        related_name="ecorenover_simulations",
    )

    def __str__(self):
        return f"{self.created_at} {self.object_id} {self.description}"
