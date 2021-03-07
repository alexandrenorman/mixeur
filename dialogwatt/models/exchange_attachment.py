# -*- coding: utf-8 -*-
from django.db import models

# import datetime

from django.utils.translation import ugettext_lazy as _
from core.models import MixeurBaseModel

# from django.core.exceptions import ValidationError


def exchange_attachment_directory_path(instance, filename):
    return "exchange/{0}/{1}".format(instance.id, filename)


class ExchangeAttachment(MixeurBaseModel):
    class Meta:
        verbose_name = _("Pièce jointe")
        verbose_name_plural = _("Pièces jointes")
        ordering = ("-created_at",)

    filecontent = models.FileField(
        upload_to=exchange_attachment_directory_path,
        blank=True,
        null=True,
        verbose_name=_("Fichier"),
    )
