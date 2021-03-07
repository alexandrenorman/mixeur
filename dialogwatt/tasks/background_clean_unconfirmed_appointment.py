# -*- coding: utf-8 -*-

import datetime
import logging

from background_task import background

from dateutil.relativedelta import relativedelta

import pytz

logger = logging.getLogger(__name__)  # NOQA


def clean_unconfirmed_appointment():
    logger.warning(
        "background_clean_unconfirmed_appointment: search appointments to delete"
    )
    from dialogwatt.models import Appointment

    appointments = Appointment.objects.filter(
        status="waiting",
        tmp_book_date__lt=datetime.datetime.now().astimezone(
            pytz.timezone("Europe/Paris")
        )
        + relativedelta(hours=-1),
    )
    if appointments.exists():
        logger.warning(
            f"background_clean_unconfirmed_appointment: Cancel unconfirmed appointements {[x.pk for x in appointments]}"
        )  # NOQA: E501
        for appointment in appointments:
            appointment.status = Appointment.CANCELLED
            appointment.save()
    else:
        logger.warning("background_clean_unconfirmed_appointment: nothing to delete")


@background(schedule=10)
def background_clean_unconfirmed_appointment():
    try:
        clean_unconfirmed_appointment()
    except Exception as e:
        import sentry_sdk

        logger.error(f"background_clean_unconfirmed_appointment {e}")
        sentry_sdk.capture_exception(e)
