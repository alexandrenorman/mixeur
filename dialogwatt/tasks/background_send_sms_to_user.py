# -*- coding: utf-8 -*-

import datetime
import logging

from background_task import background

import pytz

from twilio.base.exceptions import TwilioRestException


logger = logging.getLogger(__name__)  # NOQA


@background(schedule=10)
def background_send_sms_to_user(exchange_id):
    from dialogwatt.models import Exchange

    if Exchange.objects.filter(pk=exchange_id).exists():
        exchange = Exchange.objects.get(pk=exchange_id)
        recipient = exchange.to_account
        sender = exchange.from_account
        message = exchange.message_sms
        logger.warning(f"Send sms {sender} [{message}] -> {recipient}")
        try:
            recipient.send_sms(
                message=message, context={}, sender=sender, as_background_task=False
            )
        except TwilioRestException as e:
            exchange.error = str(e)
            exchange.save()
            return
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
