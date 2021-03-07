# -*- coding: utf-8 -*-
import datetime
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.models import User

from core.models import MixeurBaseModel

from .reason import Reason


class ActiveSlotManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(status="cancelled")


class ActiveAndFutureSlotManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .exclude(status="cancelled")
            .filter(end_date__gte=datetime.datetime.now())
        )


class SelectableSlotManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(status__in=["cancelled", "inactive"])


class SelectableForPublicSlotManager(SelectableSlotManager):
    def get_queryset(self):
        return super().get_queryset().exclude(visibility="advisor")


class Slot(MixeurBaseModel):
    class Meta:
        verbose_name = _("Créneau")
        verbose_name_plural = _("Créneaux")
        ordering = ("start_date",)

    objects = models.Manager()  # All
    active = ActiveSlotManager()  # non canceled
    active_and_future = (
        ActiveAndFutureSlotManager()
    )  # non canceled and ending later than now
    selectable = SelectableSlotManager()  # non (canceled or inactive)
    selectable_for_public = (
        SelectableForPublicSlotManager()
    )  # non (canceled or inactive)

    VISIBILITY = (
        ("online", _("Rendez-vous en ligne")),
        ("advisor", _("Rendez-vous accessible aux conseillers uniquement")),
        ("without_reservation", _("Sans rendez-vous")),
    )
    STATUS = (
        ("validated", _("Validé")),
        ("inactive", _("Désactivé")),
        ("cancelled", _("Annulé")),
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(
        _("Statut"), choices=STATUS, blank=False, max_length=100, default="validated"
    )
    sequence = models.IntegerField(
        verbose_name=_("Séquence : numéro d'update"), default=-1
    )

    text = models.CharField(_("Nom"), blank=False, max_length=100)
    group = models.ForeignKey(
        "accounts.group", verbose_name=_("Structure"), on_delete=models.CASCADE
    )

    start_date = models.DateTimeField(_("Date et heure de début"))
    end_date = models.DateTimeField(_("Date et heure de fin"))

    visibility = models.CharField(
        _("Visibilité"),
        choices=VISIBILITY,
        blank=False,
        default="online",
        max_length=30,
    )

    reasons = models.ManyToManyField(Reason, verbose_name=_("Motifs de rendez-vous"))

    place = models.ForeignKey(
        "dialogwatt.Place", on_delete=models.CASCADE, verbose_name="Lieu de conseil"
    )
    catchment_area = models.ForeignKey(
        "dialogwatt.CatchmentArea",
        on_delete=models.CASCADE,
        verbose_name="Zone de chalandise",
    )

    deadline = models.IntegerField(_("Délai (en h)"), default=24)
    time_between_slots = models.IntegerField(
        _("Temps entre deux rendez-vous (en minutes)"), default=0
    )
    use_advisor_calendar = models.BooleanField(
        _("Gestion des agendas conseillers"), default=True
    )
    number_of_active_advisors = models.IntegerField(
        _("Nombre de conseillers simultanés"), default=0
    )
    advisors = models.ManyToManyField(
        User,
        verbose_name=_("Liste de conseillers"),
        limit_choices_to=models.Q(user_type="advisor")
        | models.Q(user_type="superadvisor"),
    )
    description = models.TextField(
        verbose_name=_("Présentation interne du créneau"), blank=True
    )
    public_description = models.TextField(
        verbose_name=_("Présentation publique du créneau"), blank=True
    )

    def save(self, *args, **kwargs):
        self.sequence += 1
        return super().save(*args, **kwargs)

    @property
    def subject(self):
        return self.text

    @property
    def has_appointments(self):
        """
        Returns True if slot has non cancelled Appointments
        """
        from .appointment import Appointment

        return self.appointment_set.exclude(status=Appointment.CANCELLED).exists()

    def clean(self):
        if self.use_advisor_calendar and self.number_of_active_advisors > 0:
            raise ValidationError(
                "La gestion des agendas conseillers est incompatible avec le nombre de conseillers simultanés"
            )

        if not self.use_advisor_calendar and self.number_of_active_advisors == 0:
            raise ValidationError(
                "Le nombre de conseillers simultanés ne peut pas être égal à zéro si la gestion des agendas conseillers est désactivée"  # NOQA: E501
            )
