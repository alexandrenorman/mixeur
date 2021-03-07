# -*- coding: utf-8 -*-

import logging

from background_task import background

from messaging.external_api import SmsApi
from messaging.helpers import send_mail_immediate
from messaging.models import SmsAccount, SmtpAccount

logger = logging.getLogger(__name__)  # NOQA


@background(schedule=10)  # NOQA: CFQ002
def background_send_email_to_user(
    smtp_account,
    from_email,
    recipient_list,
    subject,
    html_message,
    ascii_message,
    attachments=None,
    system_wide_smtp_server=False,
):
    logger.warning(f"Send mail [{subject}] -> {recipient_list}")

    if smtp_account and SmtpAccount.objects.filter(pk=smtp_account).exists():
        smtp_account = SmtpAccount.objects.get(pk=smtp_account)
    else:
        smtp_account = None

    send_mail_immediate(
        smtp_account=smtp_account,
        subject=subject,
        ascii_message=ascii_message,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message,
        attachments=attachments,
        system_wide_smtp_server=system_wide_smtp_server,
    )


@background(schedule=10)
def background_send_sms_to_user(sms_account, recipient_list, ascii_message):
    logger.warning(f"Send sms [{ascii_message}] -> {recipient_list}")

    if not SmsAccount.objects.filter(pk=sms_account).exists():
        logger.error(
            f"Failed Send sms [{ascii_message}] -> {recipient_list} : no SmsAccount {sms_account}"
        )

    sms_account = SmsAccount.objects.get(pk=sms_account)

    sms_api = SmsApi(sms_account)
    for recipient in recipient_list:
        sms_api.send(recipient, ascii_message)
