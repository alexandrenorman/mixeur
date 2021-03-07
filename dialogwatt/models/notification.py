# -*- coding: utf-8 -*-
import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.models import User

from core.models import MixeurBaseModel

from .place import Place
from .reason import Reason


TRIGGER_DEFINITIONS = {
    "created_account": {
        "label": _("Création d'un compte par le contact"),
        "immediate_only": True,
    },
    "created_client": {
        "label": _("Création d'un rdv par le contact"),
        "immediate_only": True,
    },
    "changed_client": {
        "label": _("Modification d'un rdv par le contact"),
        "immediate_only": True,
    },
    "cancelled_client": {
        "label": _("Annulation d'un rdv par le contact"),
        "immediate_only": True,
    },
    "created_advisor": {
        "label": _("Création d'un rdv par le conseiller"),
        "immediate_only": True,
    },
    "changed_advisor": {
        "label": _("Modification d'un rdv par le conseiller"),
        "immediate_only": True,
    },
    "cancelled_advisor": {
        "label": _("Annulation d'un rdv par le conseiller"),
        "immediate_only": True,
    },
    "date_of_appointment": {
        "label": _("Échéance du rendez-vous"),
        "immediate_only": False,
    },
}

TRIGGER_DELAYED = [
    x for x in TRIGGER_DEFINITIONS if TRIGGER_DEFINITIONS[x]["immediate_only"] is False
]
TRIGGER_IMMEDIATE = [
    x for x in TRIGGER_DEFINITIONS if TRIGGER_DEFINITIONS[x]["immediate_only"] is True
]


class ActiveNotificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Notification(MixeurBaseModel):
    class Meta:
        verbose_name = _("Notification")

    objects = models.Manager()
    active = ActiveNotificationManager()

    TRIGGER = [(x, TRIGGER_DEFINITIONS[x]["label"]) for x in TRIGGER_DEFINITIONS]
    TO = (
        ("contact", _("Contact")),
        ("all_advisors", _("Tous les conseillers")),
        ("some_advisors", _("Des conseillers")),
        ("allocated_advisor", _("Le conseiller concerné par le rdv")),
    )
    TERM = (("immediate", _("Instantané")), ("delayed", _("Différé")))
    TERM_DAY_TYPE = (("calendar", _("Calendaire")), ("open", _("Ouvrés (hors WE)")))
    TERM_AFTER_BEFORE = (("after", _("Après")), ("before", _("Avant")))

    name = models.CharField(_("Nom de la notification"), blank=False, max_length=100)

    group = models.ForeignKey(
        "accounts.group",
        verbose_name=_("Structure"),
        on_delete=models.CASCADE,
        related_name="notification",
    )

    is_active = models.BooleanField(_("Actif ?"), default=True)

    trigger = models.CharField(
        _("Déclencheur"), choices=TRIGGER, blank=False, max_length=100
    )

    term = models.CharField(
        _("Délai"), choices=TERM, blank=False, max_length=10, default="immediate"
    )

    term_days = models.PositiveIntegerField(_("Délai en jours"), default=0)
    term_day_type = models.CharField(
        _("Type de jours de délai"),
        choices=TERM_DAY_TYPE,
        blank=False,
        max_length=10,
        default="calendar",
    )
    term_after_before = models.CharField(
        _("Avant ou après"),
        choices=TERM_AFTER_BEFORE,
        blank=False,
        max_length=10,
        default="before",
    )
    term_time = models.TimeField(_("Heure d'envoi"), default=datetime.time(12, 0))

    all_reasons = models.BooleanField(_("Tous motifs ?"), default=True)
    reasons = models.ManyToManyField(
        Reason, verbose_name=_("Motifs de rendez-vous"), related_name="notification"
    )

    all_places = models.BooleanField(_("Tous lieux ?"), default=True)
    places = models.ManyToManyField(
        Place, verbose_name="Lieux de conseil", related_name="notification"
    )

    to = models.CharField(_("Destinataire"), choices=TO, blank=False, max_length=100)
    advisors = models.ManyToManyField(
        User, verbose_name=_("Conseillers"), related_name="notification"
    )

    sms_is_active = models.BooleanField(_("Sms actif ?"), default=True)
    sms_message = models.TextField(verbose_name=_("Texte SMS"), blank=True)

    mail_is_active = models.BooleanField(_("Mail actif ?"), default=True)
    mail_subject = models.CharField(
        verbose_name=_("Sujet du MAIL"), blank=True, max_length=200
    )
    mail_message = models.TextField(verbose_name=_("Texte MAIL"), blank=True)

    chat_is_active = models.BooleanField(_("Chat actif ?"), default=False)
    chat_message = models.TextField(verbose_name=_("Texte CHAT"), blank=True)

    def clean(self):
        if self.trigger == "created_account" and self.term != "immediate":
            raise ValidationError(
                "Les notifications de création de compte doivent utiliser un délai instantané"
            )

        if self.term == "delayed":
            if self.term_days == 0:
                raise ValidationError(
                    "Un traitement différé nécessite un délai au moins égal à un jour"
                )

        if (
            not self.sms_is_active
            and not self.mail_is_active
            and not self.chat_is_active
        ):
            raise ValidationError("Au moins une notification doit être active")
