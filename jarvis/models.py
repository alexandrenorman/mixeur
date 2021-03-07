# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


from core.models import MixeurBaseModel


class ActiveAllowedSenderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class AllowedSender(MixeurBaseModel):
    class Meta:
        verbose_name = _("Utilisateurs externes autorisé Jarvis/Chef")

    active = ActiveAllowedSenderManager()

    is_active = models.BooleanField(
        _("active"), default=True, help_text=_("Active allowed sender ?")
    )
    group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe"),
        help_text=_("Structure concernée"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="jarvis_allowed_sender",
    )
    email = models.EmailField(unique=True)
