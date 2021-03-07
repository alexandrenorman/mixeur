# -*- coding: utf-8 -*-
import logging
import os
from typing import Any, List, Union

from django.core.mail import EmailMultiAlternatives, get_connection
from django.template import Context, Template, loader

import html2text


from premailer import transform

from config.settings import DEFAULT_FROM_EMAIL, DEFAULT_FROM_EMAIL_NAME

from messaging.external_api import SmsApi
from messaging.models import SmsAccount, SmtpAccount

from white_labelling.models import WhiteLabelling

# https://anymail.readthedocs.io/en/stable/tips/multiple_backends/

logger = logging.getLogger(__name__)  # NOQA


def get_smtp_connection(smtp_account: Union[SmtpAccount, None]) -> Any:
    """
    return Smtp Connection to use for SmtpAccount
    """
    if smtp_account is None:
        connection = get_connection("django.core.mail.backends.smtp.EmailBackend")
        return connection

    if not smtp_account.is_active:
        raise ValueError("SmtpAccount is not active")

    if smtp_account.smtp_type == "mailgun":
        connection = get_connection(
            "anymail.backends.mailgun.EmailBackend", api_key=smtp_account.mailgun_apikey
        )

    elif smtp_account.smtp_type == "smtp":
        connection = get_connection(
            "django.core.mail.backends.smtp.EmailBackend",
            host=smtp_account.email_host,
            port=smtp_account.email_port,
            username=smtp_account.email_host_user,
            password=smtp_account.email_host_password,
            use_tls=smtp_account.email_use_tls,
            use_ssl=smtp_account.email_use_ssl,
        )
    else:
        raise ValueError(
            f"unknown smtp_type for SmtpAccount {smtp_account.pk} / {smtp_account.smtp_type}"
        )

    return connection


def send_mail_immediate(  # NOQA: CFQ002
    smtp_account: Union[SmtpAccount, None],
    subject: str,
    ascii_message: str,
    from_email: str,
    recipient_list: List,
    html_message: str,
    attachments: List = None,
    system_wide_smtp_server: bool = False,
) -> None:
    if not system_wide_smtp_server:
        if smtp_account is not None:
            connection = get_smtp_connection(smtp_account)
        else:
            connection = None
    else:
        connection = None
        from_email = DEFAULT_FROM_EMAIL

    msg = EmailMultiAlternatives(
        subject=subject,
        body=ascii_message,
        from_email=from_email,
        to=recipient_list,
        connection=connection,
    )
    msg.attach_alternative(html_message, "text/html")
    if attachments:
        import quopri

        for f in attachments:
            msg.attach(
                filename=f["filename"],
                content=quopri.decodestring(f["content"]),
                mimetype=f["mimetype"],
            )

    msg.send()


class WhiteLabellingHelperMixin:
    class Meta:
        abstract = True

    def _white_labelling_to_use(
        self, white_labelling: Union[WhiteLabelling, None] = None
    ) -> Union[WhiteLabelling, None]:
        """
        Return WhiteLabelling to use, depending on account preference

        :white_labelling: white_labelling.WhiteLabelling (optionnal)
        """
        if white_labelling is not None:
            return white_labelling

        pwl = self.account.preferred_white_labelling
        if pwl is not None:
            return pwl

        if WhiteLabelling.objects.filter(is_default=True, is_active=True).exists():
            return WhiteLabelling.objects.filter(
                is_default=True, is_active=True
            ).first()

        return None


class EmailToUserHelper(WhiteLabellingHelperMixin):
    """
    Send an email to an account.User or a fac.Contact
    """

    def __init__(
        self, account: Any, white_labelling: Union[WhiteLabelling, None] = None
    ) -> None:
        """
        :account: accounts.User or fac.Contact recipient
        :white_labelling: white_labelling.WhiteLabelling (optionnal)
        """
        self.account = account
        self.white_labelling = self._white_labelling_to_use(white_labelling)
        self.smtp_account = None
        self.context = {}
        self.sender = None

    def send_email(  # NOQA: CFQ002
        self,
        subject: str,
        message: str,
        context: dict = None,
        sender: Any = None,
        as_background_task: bool = True,
        use_fallback: bool = True,
        attachments: list = None,
        system_wide_smtp_server: bool = False,
    ) -> Any:
        """
        Send email using background task

        :subject:
        :message:
        :context:
        :sender:
        :as_background_task:
        :use_fallback:
        :attachments:
        :system_wide_smtp_server: force default stmp server
        """
        self.context = context or {}
        self.sender = sender
        if not system_wide_smtp_server:
            smtp_account = self._get_smtp_account()
            if smtp_account is None and not use_fallback:
                logger.warning(
                    f"No SmtpAccount configured and not allowed to use fallback {sender} {subject}"
                )
                raise ValueError("No active SMTP connection to use")

        else:
            smtp_account = None

        formatted_subject = self._format_subject(subject)
        formatted_message = self._format_html_message(message)
        ascii_message = html2text.html2text(formatted_message)

        if as_background_task:
            task = self._background_send_email_to_user(
                smtp_account=smtp_account.pk if smtp_account is not None else None,
                from_email=self._from_field,
                recipient_list=[self.account.email],
                subject=formatted_subject,
                html_message=formatted_message,
                ascii_message=ascii_message,
                attachments=attachments,
                system_wide_smtp_server=system_wide_smtp_server,
            )
            return task
        else:
            send_mail_immediate(
                smtp_account=smtp_account,
                subject=subject,
                ascii_message=ascii_message,
                from_email=self._from_field,
                recipient_list=[self.account.email],
                html_message=formatted_message,
                attachments=attachments,
                system_wide_smtp_server=system_wide_smtp_server,
            )

    def _background_send_email_to_user(  # NOQA: CFQ002
        self: str,
        smtp_account: Any,
        from_email: str,
        recipient_list: List,
        subject: str,
        html_message: str,
        ascii_message: str,
        attachments: List,
        system_wide_smtp_server: bool = False,
    ) -> None:
        """
        Send a mail using a background task
        """
        from messaging.tasks import background_send_email_to_user

        task = background_send_email_to_user(
            smtp_account=smtp_account,
            from_email=self._from_field,
            recipient_list=recipient_list,
            subject=subject,
            html_message=html_message,
            ascii_message=ascii_message,
            attachments=attachments,
            system_wide_smtp_server=system_wide_smtp_server,
        )
        return task

    @property
    def _from_field(self) -> str:
        """
        Formated sender (from smtp connection) field as "name" <email>
        """
        return f"{self._from_name} <{self._from_email}>"

    @property
    def _from_name(self) -> str:
        """
        Name of sender from smtp connection
        """
        if self.smtp_account is None:
            self._get_smtp_account()
        if self.smtp_account is not None:
            return self.smtp_account.from_username

        return DEFAULT_FROM_EMAIL_NAME

    @property
    def _from_email(self) -> str:
        """
        Email of sender from smtp connection
        """
        if self.smtp_account is None:
            self._get_smtp_account()
        if self.smtp_account is not None:
            return self.smtp_account.email_host_user

        return DEFAULT_FROM_EMAIL

    def _get_smtp_account_from_group(self, group) -> Union[SmtpAccount, None]:
        # Specified SmtpAccount for the group
        if SmtpAccount.objects.filter(group=group).exists():
            self.smtp_account = SmtpAccount.objects.filter(group=group).first()
            return self.smtp_account

        # SmtpAccount for group's WhiteLabelling
        if not SmtpAccount.objects.filter(group=group).exists():
            if (
                group.preferred_white_labelling
                and group.preferred_white_labelling.smtp_account
            ):
                self.smtp_account = group.preferred_white_labelling.smtp_account
                return self.smtp_account

        return None

    def _get_smtp_account(self) -> Union[SmtpAccount, None]:
        """
        Return the SmtpAccount to use or None

        If sender is supplied and expert:
        - SmtpAccount for the sender
        Else if account.is_expert return first of:
        - SmtpAccount for the group
        - SmtpAccount for the prefered WhiteLabelling of the group
        - SmtpAccount for the specified WhiteLabelling
        - SmtpAccount for the default WhiteLabelling
        - None
        else:
        - SmtpAccount for the specified WhiteLabelling
        - SmtpAccount for the default WhiteLabelling
        - None
        """
        if self.sender and self.sender.is_expert:
            smtp_account = self._get_smtp_account_from_group(self.sender.group)
            if smtp_account:
                return smtp_account

        if self.account.is_expert:
            smtp_account = self._get_smtp_account_from_group(self.account.group)
            if smtp_account:
                return smtp_account

        # SmtpAccount for specified WhiteLabelling
        if self.white_labelling and self.white_labelling.smtp_account:
            self.smtp_account = self.white_labelling.smtp_account
            return self.smtp_account

        # SmtpAccount for default WhiteLabelling
        qs = SmtpAccount.system_wide.filter(white_labelling__is_default=True)
        if qs.exists():
            return qs.first()

        self.smtp_account = None
        return self.smtp_account

    def _template_path(self, filename: str) -> str:
        """
        return existing pathname for given template

        either in WhiteLabelling.cdn_directory_path or "messaging/templates/messaging/"
        """
        if self.white_labelling is not None:
            template_path = os.path.join(
                self.white_labelling.cdn_directory_path, filename
            )
            if os.path.lexists(template_path):
                return template_path

        return f"/app/django/messaging/templates/messaging/{filename}"

    def _format_subject(self, subject: str) -> str:
        """
        format subject using template mail_subject.html and global context
        """
        subject_template_path = self._template_path("mail_subject.txt")
        if self.white_labelling is not None:
            domain = self.white_labelling.domain
            site_name = self.white_labelling.site_title
        else:
            domain = "mixeur-prod.hespul.org"
            site_name = "mixeur"

        self.context.update(
            {"domain": domain, "site_name": site_name, "protocol": "https"}
        )
        self.context.update(
            {"subject": Template(subject).render(Context(self.context))}
        )
        subject = loader.render_to_string(subject_template_path, self.context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        return subject

    def _format_html_message(self, message: str) -> str:
        """
        format message as html using template mail_body.html and mail_style.css and global context,
        pass it through premailer
        """
        template_path = self._template_path("mail_body.html")
        stylesheet_path = self._template_path("mail_style.css")
        stylesheet = open(stylesheet_path, "r").read()

        if self.white_labelling is not None:
            domain = self.white_labelling.domain
            site_name = self.white_labelling.site_title
        else:
            domain = "mixeur-prod.hespul.org"
            site_name = "mixeur"

        self.context.update(
            {
                "domain": domain,
                "site_name": site_name,
                "protocol": "https",
                "stylesheet": stylesheet,
            }
        )

        self.context.update(
            {"message": Template(message).render(Context(self.context))}
        )

        template = Template(open(template_path, "r").read())

        message_html = template.render(Context(self.context))

        html_premailed = transform(message_html)
        return html_premailed


class SmsToUserHelper(WhiteLabellingHelperMixin):
    """
    Send a sms to an account.User or a fac.Contact
    """

    def __init__(
        self, account: Any, white_labelling: Union[WhiteLabelling, None] = None
    ) -> None:
        """
        :account: accounts.User  or fac.Contact recipient
        :white_labelling: white_labelling.WhiteLabelling (optionnal)
        """
        self.account = account
        self.white_labelling = self._white_labelling_to_use(white_labelling)
        self.smtp_account = None
        self.context = {}
        self.sender = None

    def send_sms(  # NOQA: C901
        self,
        message: str,
        context: dict = None,
        sender: Any = None,
        as_background_task: bool = True,
    ) -> Any:
        """
        Send sms using background task

        :message:
        :context:
        :sender:
        :as_background_task:
        """
        self.context = context or {}
        self.sender = sender

        if self.white_labelling is not None:
            domain = self.white_labelling.domain
            site_name = self.white_labelling.site_title
        else:
            domain = "prod.mixeur.solutions"
            site_name = "mixeur"

        self.context.update(
            {"domain": domain, "site_name": site_name, "protocol": "https"}
        )

        ascii_message = Template(message).render(Context(self.context))

        sms_account = self._get_sms_account()

        if not sms_account:
            raise ValueError("Il n'y a pas de compte d'envoi de SMS disponible.")

        if not sms_account.can_send_sms:
            raise ValueError(
                f"Le nombre maximal de sms mensuel a été atteint ({sms_account.monthly_limit})."
            )

        if not self.account.allow_to_use_phone_number_to_send_reminder:
            raise ValueError(
                f"Il n'est pas possible d'envoyer un mail à cet utilisateur email: {self.account.email} / téléphone: {self.account.phone} / permission rgpd: {self.account.last_rgpd_consent.allow_to_use_phone_number_to_send_reminder}."  # NOQA: E501
            )

        from accounts.models import User
        from dialogwatt.models import FacContactForDialogwatt

        if type(self.account) is FacContactForDialogwatt:
            if self.account.mobile_phone:
                phone = self.account.mobile_phone.as_e164
            elif self.account.phone:
                phone = self.account.phone.as_e164

        if type(self.account) is User:
            phone = self.account.phone.as_e164

        if as_background_task:
            task = self._background_send_sms_to_user(
                sms_account=sms_account.pk if sms_account is not None else None,
                recipient_list=[phone],
                ascii_message=ascii_message,
            )
            return task

        else:
            sms_api = SmsApi(sms_account)
            for recipient in [phone]:
                sms_api.send(recipient, ascii_message)

    def _background_send_sms_to_user(
        self: str, sms_account: Any, recipient_list: List, ascii_message: str
    ) -> None:
        """
        Send a mail using a background task
        """
        from messaging.tasks import background_send_sms_to_user

        task = background_send_sms_to_user(
            sms_account=sms_account,
            recipient_list=recipient_list,
            ascii_message=ascii_message,
        )
        return task

    def _get_sms_account_from_group(self, group) -> Union[SmsAccount, None]:
        # Specified SmsAccount for the group
        if SmsAccount.objects.filter(group=group).exists():
            self.sms_account = SmsAccount.objects.filter(group=group).first()
            return self.sms_account

        return None

    def _get_sms_account(self) -> Union[SmsAccount, None]:
        """
        Return the SmsAccount to use (from group) or None
        """
        if self.sender and self.sender.is_expert:
            self.sms_account = self._get_sms_account_from_group(self.sender.group)
            if self.sms_account:
                return self.sms_account

        if self.account.is_expert:
            self.sms_account = self._get_sms_account_from_group(self.account.group)
            if self.sms_account:
                return self.sms_account

        if self.account.is_client:
            return self.account.white_labelling.sms_account

        return None
