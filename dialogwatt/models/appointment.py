# -*- coding: utf-8 -*-
import uuid
from datetime import datetime


from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

import pytz

from accounts.models import User

from core.models import MixeurBaseModel

from dialogwatt.fields.client_or_contact_field import ClientOrContactGenericForeignKey

from helpers.mixins.mixins_recordable import RecordableModelMixin

from .notification_requested import NotificationRequested
from .place import Place
from .reason import Reason
from .slot import Slot


class ActiveAppointmentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(status=Appointment.CANCELLED)


class ActiveAndFutureAppointmentManager(ActiveAppointmentManager):
    def get_queryset(self):
        now = datetime.now().astimezone(pytz.timezone("Europe/Paris"))
        return super().get_queryset().filter(start_date__gte=now)


class ActiveTodayAndAfterAppointmentManager(ActiveAppointmentManager):
    def get_queryset(self):
        now = datetime.now().astimezone(pytz.timezone("Europe/Paris")).date()
        return super().get_queryset().filter(start_date__gte=now)


class Appointment(RecordableModelMixin, MixeurBaseModel):
    class Meta:
        verbose_name = _("Rendez-vous")
        verbose_name_plural = _("Rendez-vous")
        ordering = ("start_date",)

    objects = models.Manager()
    active = ActiveAppointmentManager()
    active_and_future = ActiveAndFutureAppointmentManager()
    active_today_and_after = ActiveTodayAndAfterAppointmentManager()

    WAITING = "waiting"
    VALIDATED = "validated"
    CANCELLED = "cancelled"

    STATUS = (
        (WAITING, _("En attente de validation")),
        (VALIDATED, _("Validé")),
        (CANCELLED, _("Annulé")),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(
        _("Statut"), choices=STATUS, blank=False, max_length=100, default="validated"
    )

    subject = models.CharField(
        verbose_name=_("Sujet"), blank=False, null=False, max_length=100
    )

    start_date = models.DateTimeField(_("Date et heure de début"))
    end_date = models.DateTimeField(_("Date et heure de fin"))
    tmp_book_date = models.DateTimeField(
        _("Date et heure de réservation temporaire"), null=True
    )

    sequence = models.IntegerField(
        verbose_name=_("Séquence : numéro d'update"), default=-1
    )

    advisor = models.ForeignKey(
        User,
        verbose_name=_("Conseiller"),
        limit_choices_to=models.Q(user_type="advisor")
        | models.Q(user_type="superadvisor"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="apointments_as_advisor",
    )

    content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    client_or_contact = ClientOrContactGenericForeignKey("content_type", "object_id")

    place = models.ForeignKey(
        Place, verbose_name=_("Lieu"), null=True, on_delete=models.SET_NULL
    )
    slot = models.ForeignKey(
        Slot, verbose_name=_("Créneau"), null=True, on_delete=models.SET_NULL
    )
    reason = models.ForeignKey(
        Reason, verbose_name=_("Motif"), null=True, on_delete=models.SET_NULL
    )
    description = models.TextField(verbose_name=_("Description"), blank=True)
    has_been_honored = models.BooleanField(
        verbose_name=_("Rendez-vous honoré ?"), default=False
    )

    notification_requested = GenericRelation(NotificationRequested)

    form_answers = JSONField(blank=True, null=True)

    @property
    def group(self):
        if self.slot:
            return self.slot.group

        elif self.advisor:
            return self.advisor.group

        elif self.reason:
            return self.reason.group

        else:
            raise ValueError("Le RDV n'est rattaché à aucun groupe.")

    def save(self, *args, **kwargs):
        self.sequence += 1
        return super().save(*args, **kwargs)
