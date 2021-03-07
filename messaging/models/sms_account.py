# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError

from django.utils.translation import ugettext_lazy as _
from core.models import MixeurBaseModel

# from phonenumber_field.modelfields import PhoneNumberField


class SmsAccount(MixeurBaseModel):
    class Meta:
        verbose_name = _("Compte envois de SMS")

    ACCOUNT_TYPES = (
        ("twilio", "Twilio"),
        ("ovh", "OVH"),
        ("mail", "mail backend for debug"),
    )

    account_type = models.CharField(
        _("Type de serveur mail"), choices=ACCOUNT_TYPES, default="ovh", max_length=20
    )

    twilio_account = models.CharField(
        _("Compte Twilio"), blank=True, null=True, max_length=100
    )
    twilio_token = models.CharField(
        _("Token Twilio"), blank=True, null=True, max_length=100
    )

    ovh_account = models.CharField(
        _("Compte OVH"), blank=True, null=True, max_length=100
    )
    ovh_login = models.CharField(
        _("Identifiant OVH"), blank=True, null=True, max_length=100
    )
    ovh_password = models.CharField(
        _("Mot de passe OVH"), blank=True, null=True, max_length=100
    )
    ovh_sender = models.CharField(
        _("Expéditeur"), blank=True, null=True, max_length=100
    )

    phone = models.CharField(
        _("Numéro de téléphone d'expédition"), max_length=100, blank=True, null=True
    )
    group = models.OneToOneField(
        "accounts.group",
        verbose_name=_("Structure"),
        on_delete=models.CASCADE,
        related_name="messaging_sms_account",
    )
    is_active = models.BooleanField(
        _("active"), default=True, help_text=_("Compte actif ?")
    )
    monthly_limit = models.IntegerField(
        verbose_name=_("Limite mensuelle de sms envoyés"), default=1000
    )

    def clean(self):
        if self.account_type == "twilio":
            if not (self.twilio_account and self.twilio_token and self.phone):
                raise ValidationError(
                    "Pour un compte de type Twilio, vous devez spécifier le compte, le token et le numéro de téléphone"
                )

        if self.account_type == "ovh":
            if not (
                self.ovh_account
                and self.ovh_login
                and self.ovh_password
                and self.ovh_sender
            ):
                raise ValidationError(
                    "Pour un compte de type OVH, vous devez spécifier le compte, l'identifiant, le mot de passe et l'identifiant d'expedition"  # NOQA: E501
                )

    @property
    def can_send_sms(self) -> bool:
        return self.monthly_sent <= self.monthly_limit

    @property
    def monthly_sent(self) -> int:
        return self.monthly_sent_on_month(month=datetime.now())

    def monthly_sent_on_month(self, month: datetime) -> int:
        from dialogwatt.models import Exchange

        exchanges_count = Exchange.objects.filter(
            from_account__group=self.group,
            message_type="sms",
            has_been_sent_on__year=month.year,
            has_been_sent_on__month=month.month,
        ).count()
        return exchanges_count

    def __str__(self):
        return self.group.name
