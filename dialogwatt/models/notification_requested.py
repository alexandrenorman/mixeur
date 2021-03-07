# -*- coding: utf-8 -*-
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel

from .exchange import Exchange
from .notification import Notification


class NotificationRequested(MixeurBaseModel):
    """
    Keep track of object for which we have done a notification
    """

    class Meta:
        verbose_name = _("Notification demandées")

    notification = models.ForeignKey(
        Notification, verbose_name=_("Notification"), on_delete=models.CASCADE
    )

    exchange = models.ForeignKey(
        Exchange, verbose_name=_("Message"), on_delete=models.CASCADE
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="notification",
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)

    # Object for which we do a notification
    origin_of_notification = GenericForeignKey("content_type", "object_id")
