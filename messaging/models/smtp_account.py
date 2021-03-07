# -*- coding: utf-8 -*-
from django.db import models

from django.utils.translation import ugettext_lazy as _
from core.models import MixeurBaseModel


class SmtpAccountActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, group=None)


class SmtpAccount(MixeurBaseModel):
    class Meta:
        verbose_name = _("Configuration SMTP/Mailgun")

    system_wide = SmtpAccountActiveManager()
    objects = models.Manager()

    SMTP_TYPES = (("mailgun", "Mailgun"), ("smtp", "SMTP"))

    is_active = models.BooleanField(
        _("active"), default=True, help_text=_("Compte actif ?")
    )

    name = models.CharField(
        _("Nom de la configuration"), max_length=100, default="Configuration SMTP"
    )

    group = models.OneToOneField(
        "accounts.group",
        verbose_name=_("Structure"),
        on_delete=models.CASCADE,
        related_name="messaging_smtp_account",
        null=True,
        blank=True,
        help_text=_(
            "Si aucune structure n'est sélectionnée, il s'agit d'une configuration globale"
        ),
    )

    from_username = models.CharField(
        _("Nom d'expéditeur affiché"), blank=True, max_length=100, default=""
    )

    smtp_type = models.CharField(
        _("Type de serveur mail"), choices=SMTP_TYPES, default="smtp", max_length=20
    )

    mailgun_apikey = models.CharField(_("Clef d'API"), blank=True, max_length=100)
    mailgun_monthly_limit = models.IntegerField(
        verbose_name=_("Limite mensuelle d'envois"), default=10000
    )

    email_host = models.CharField(_("SMTP serveur"), blank=True, max_length=100)
    email_port = models.IntegerField(verbose_name=_("SMTP port"), default=25)
    email_host_user = models.CharField(
        _("SMTP utilisateur"), blank=True, max_length=100
    )
    email_host_password = models.CharField(
        _("SMTP mot de passe"), blank=True, max_length=100
    )
    email_use_tls = models.BooleanField(_("SMTP utiliser TLS"), default=False)
    email_use_ssl = models.BooleanField(_("SMTP utiliser SSL"), default=False)

    def __str__(self):
        return self.name
