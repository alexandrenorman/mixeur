# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import MixeurBaseModel


class LogUser(MixeurBaseModel):
    user = models.ForeignKey(
        "accounts.User",
        verbose_name=_("Utilisateur"),
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="log_user",
    )

    white_labelling = models.ForeignKey(
        "white_labelling.WhiteLabelling",
        verbose_name=_("Domaine / marque blanche"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="log_user_wl",
    )
