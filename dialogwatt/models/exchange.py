# -*- coding: utf-8 -*-
from background_task.tasks import Task

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel

from dialogwatt.fields.client_or_contact_field import ClientOrContactGenericForeignKey
from dialogwatt.models.fac_contact_for_dialogwatt import FacContactForDialogwatt
from dialogwatt.tasks import background_send_email_to_user, background_send_sms_to_user

from fac.models import Note

from .exchange_attachment import ExchangeAttachment


class Exchange(MixeurBaseModel):
    class Meta:
        verbose_name = _("Exchange")
        ordering = ("-created_at",)

    MESSAGE_TYPE = (("sms", _("SMS")), ("mail", _("Courriel")), ("chat", _("Chat")))

    group = models.ForeignKey(
        "accounts.group",
        verbose_name=_("Structure"),
        on_delete=models.CASCADE,
    )

    schedule = models.DateTimeField(
        verbose_name="Date d'envoi programmée", default=timezone.now
    )
    background_task = models.ForeignKey(
        Task,
        verbose_name=_("Background Task"),
        on_delete=models.SET_NULL,
        related_name="background_task",
        null=True,
    )
    from_account = models.ForeignKey(
        "accounts.user",
        verbose_name=_("Expediteur"),
        on_delete=models.SET_NULL,
        related_name="exchange_from",
        null=True,
    )
    content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    to_account = ClientOrContactGenericForeignKey("content_type", "object_id")

    trigger = models.CharField(_("Déclencheur"), blank=True, null=True, max_length=100)
    subject = models.CharField(_("Sujet"), blank=True, null=True, max_length=100)
    message_sms = models.TextField(verbose_name=_("Message SMS"), blank=True, null=True)
    message_mail_ascii = models.TextField(
        verbose_name=_("Message mail plaintext"), blank=True, null=True
    )
    message_mail_html = models.TextField(
        verbose_name=_("Message mail html"), blank=True, null=True
    )

    message_type = models.CharField(
        _("Type de message"), choices=MESSAGE_TYPE, blank=True, null=True, max_length=10
    )
    # has_been_sent = models.BooleanField(_("A été envoyé ?"), default=False)
    has_been_sent_on = models.DateTimeField(blank=True, null=True)

    # has_been_received = models.BooleanField(_("A été reçu ?"), default=False)
    has_been_received_on = models.DateTimeField(blank=True, null=True)

    # has_been_opened = models.BooleanField(_("A été ouvert ?"), default=False)
    has_been_opened_on = models.DateTimeField(blank=True, null=True)

    attachments = models.ManyToManyField(
        ExchangeAttachment, verbose_name=_("Fichiers joints")
    )

    error = models.TextField(_("Message d'erreur"), blank=True, null=True)

    def clean(self):
        if self.message_type == "sms":
            if self.subject:
                raise ValidationError(_("Un sms ne peut pas avoir de sujet"))
            if self.attachments.exists():
                raise ValidationError(
                    _("Un sms ne peut pas avoir de fichiers attachés")
                )

    def save_as_contact_note(self) -> None:
        if type(self.to_account) is FacContactForDialogwatt:
            contact = self.to_account
            Note.objects.create(
                owning_group=contact.owning_group,
                creator=self.from_account,
                linked_object=contact,
                note=f"""<p>
Sujet (Dialogwatt): {self.subject}<br>
{self.message_mail_html}
</p>
                """,
            )

    def send_by_sms(self) -> None:
        if not self.to_account.allow_to_use_phone_number_to_send_reminder:
            self.error = "L'utilisateur n'autorise pas que son numéro de téléphone soit utilisé (RGPD)"
            self.message_type = "sms"
            self.save()
            raise ValueError(self.error)

        if not self.to_account.mobile_phone:
            self.error = "L'utilisateur n'a pas de numéro de téléphone mobile"
            self.message_type = "sms"
            self.save()
            raise ValueError(self.error)

        if not (
            self.group
            and self.group.messaging_sms_account
            and self.group.messaging_sms_account.is_active
        ):
            self.error = "L'expéditeur n'a pas de compte d'envoi de sms actif"
            self.save()
            raise ValueError(self.error)

        self.background_task = background_send_sms_to_user(
            exchange_id=self.pk, schedule=self.schedule
        )

        self.error = ""
        self.message_type = "sms"
        self.save()

    def send_by_email(self) -> None:
        if not self.to_account.allow_to_use_email_to_send_reminder:
            self.error = (
                "L'utilisateur n'autorise pas que son courriel soit utilisé (RGPD)"
            )
            self.message_type = "mail"
            self.save()
            raise ValueError(self.error)

        self.background_task = background_send_email_to_user(
            exchange_id=self.pk, schedule=self.schedule
        )

        self.error = ""
        self.message_type = "mail"
        self.save()

    def send_by_chat(self) -> None:
        self.error = "Not implemented yet"
        self.save()
        raise ValueError(self.error)

    @property
    def has_been_sent(self):
        if (
            self.has_been_sent_on is not None
            and not Task.objects.filter(pk=self.background_task.pk).exists()
        ):
            return True

        return False
