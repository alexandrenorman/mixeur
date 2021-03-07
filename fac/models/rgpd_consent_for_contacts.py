# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class RgpdConsentForContacts(models.Model):
    class Meta:
        verbose_name = _("RgpdConsent")
        verbose_name_plural = _("RgpdConsents")
        ordering = ["-creation_date"]

    def __str__(self):
        return f"{self.creation_date}"

    contact = models.ForeignKey("fac.contact", on_delete=models.CASCADE)

    creation_date = models.DateTimeField(
        verbose_name=_("Date de création"), auto_now_add=True
    )
    allow_to_keep_data = models.BooleanField(
        _("Permettre la conservation de mes données dans le système de traitement."),
        default=True,
    )
    allow_to_use_email_to_send_reminder = models.BooleanField(
        _(
            "Permettre l'utilisation de mon email pour envoyer un rappel de rendez-vous ou des informations liées à mon dossier."  # NOQA: E501
        ),
        default=True,
    )
    allow_to_use_phone_number_to_send_reminder = models.BooleanField(
        _(
            "Permettre l'utilisation de mon numéro de téléphone pour envoyer un rappel de rendez-vous."
        ),
        default=True,
    )
    allow_to_share_my_information_with_my_advisor = models.BooleanField(
        _("Permettre le partage de mes informations avec l'EIE qui suit mon dossier."),
        default=True,
    )
    allow_to_share_my_information_with_partners = models.BooleanField(
        _(
            "Permettre le partage de mes informations avec nos partenaires à des fins statistiques."
        ),
        default=True,
    )
