# -*- coding: utf-8 -*-

import datetime
import logging

from background_task import background

import pytz


logger = logging.getLogger(__name__)  # NOQA


@background(schedule=10)
def background_send_email_to_user(exchange_id):
    from dialogwatt.models import Exchange

    if Exchange.objects.filter(pk=exchange_id).exists():
        exchange = Exchange.objects.get(pk=exchange_id)
        recipient = exchange.to_account
        sender = exchange.from_account
        if sender is None:
            sender = exchange.group.users[0]

        subject = exchange.subject
        message = exchange.message_mail_html
        if sender:
            logger.warning(f"Send mail {sender.email} [{subject}] -> {recipient.email}")
        else:
            logger.warning(f"Send mail unknown sender [{subject}] -> {recipient.email}")

        try:

            recipient.send_email(
                subject=subject,
                html_message=message,
                context={},
                sender=sender,
                as_background_task=False,
                use_fallback=False,
            )

        except Exception as e:
            exchange.error = str(e)
        else:
            exchange.has_been_sent_on = datetime.datetime.now().astimezone(
                pytz.timezone("Europe/Paris")
            )
        finally:
            exchange.save()
            exchange.save_as_contact_note()
    else:
        logger.error(f"Exchange {exchange_id} does not exists")

    return
