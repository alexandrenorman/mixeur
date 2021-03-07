# -*- coding: utf-8 -*-
import datetime

import recurrence.fields

from core.models import MixeurBaseModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from helpers.models import representation_helper

from .contact import Contact
from .organization import Organization


class ReminderQueryset(models.QuerySet):
    def accessible_by(self, user):
        if user.is_administrator:
            return self

        return self.filter(owning_group=user.group)


class ReminderManager(models.Manager.from_queryset(ReminderQueryset)):
    """
    reminder manager for reminders to be handled quickly
    """

    def callout(self):
        return self.filter(done=False, date__lte=datetime.date.today()).exclude(
            date=None
        )


@representation_helper
class Reminder(MixeurBaseModel):
    """
    Reminder to Note or Action
    """

    objects = ReminderManager()

    class Meta:
        verbose_name = _("Reminder")
        verbose_name_plural = _("Reminders")

    owning_group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe propriétaire"),
        on_delete=models.CASCADE,
        null=False,
        related_name="reminders",
    )

    creator = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        verbose_name=_("Createur"),
        blank=True,
        null=True,
    )

    content_type_task = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="content_type_task",
    )
    object_id_task = models.PositiveIntegerField(blank=True, null=True)
    # linked note or action (and maybe other models later on)
    linked_object_task = GenericForeignKey("content_type_task", "object_id_task")

    content_type_contactable = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="content_type_contactable",
    )
    object_id_contactable = models.PositiveIntegerField(blank=True, null=True)
    # linked organization or contact (and maybe other models later on)
    linked_object_contactable = GenericForeignKey(
        "content_type_contactable", "object_id_contactable"
    )

    done = models.BooleanField(verbose_name=_("Le rappel est traité"), default=False)
    date = models.DateField(verbose_name=_("Date de rappel"), blank=True, null=True)
    persons = models.ManyToManyField(
        "accounts.User",
        verbose_name=_("Qui rappeler ?"),
        default=None,
        related_name="reminder_persons",
        blank=True,
    )
    recurrences = recurrence.fields.RecurrenceField(blank=True, null=True)

    def __str__(self):
        return f"Reminder - {self.linked_object_task}"

    @property
    def linked_object_name(self):
        if type(self.linked_object_contactable) is Contact:
            return self.linked_object_contactable.full_name

        if type(self.linked_object_contactable) is Organization:
            return self.linked_object_contactable.name

        return ""

    @property
    def contactable_type(self):
        return self.linked_object_contactable.__class__.__name__

    @property
    def object_type(self):
        return self.linked_object_task.__class__.__name__
