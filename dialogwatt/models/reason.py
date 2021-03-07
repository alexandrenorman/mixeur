# -*- coding: utf-8 -*-
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel


class ActiveReasonManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Reason(MixeurBaseModel):
    class Meta:
        verbose_name = _("Motif de rendez-vous")
        verbose_name_plural = _("Motifs de rendez-vous")
        ordering = ("name",)

    objects = models.Manager()
    active = ActiveReasonManager()

    name = models.CharField(_("Nom du service"), blank=False, max_length=100)
    color = models.CharField(_("Color"), blank=False, max_length=10, default="#888888")
    is_active = models.BooleanField(_("Actif ?"), default=True)

    duration = models.IntegerField(_("Durée (en minutes)"), default=0)

    group = models.ForeignKey(
        "accounts.group", verbose_name=_("Structure"), on_delete=models.CASCADE
    )

    internal_description = models.TextField(
        verbose_name=_("Présentation interne service"), blank=True, null=True
    )

    show_description = models.BooleanField(
        _("Montrer la description du service"), default=True
    )
    description = models.TextField(
        verbose_name=_("Présentation du service"), blank=True, null=True
    )

    form = JSONField(blank=True, null=True)
