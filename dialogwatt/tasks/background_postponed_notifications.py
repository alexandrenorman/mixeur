# -*- coding: utf-8 -*-

import logging

from background_task import background

logger = logging.getLogger(__name__)  # NOQA


def postponed_notifications():
    logger.warning("Launch background postponed notifications FAIL")
    from dialogwatt.helpers.notification_manager import NotificationManager
    from dialogwatt.models import Appointment
    from dialogwatt.models.notification import TRIGGER_DELAYED

    logger.warning("Launch background postponed notifications")
    notification_manager = NotificationManager(immediate_only=False)

    for appointment in Appointment.active_today_and_after.all():
        for trigger_type in TRIGGER_DELAYED:
            logger.debug(f" - Appointment {appointment.pk} / {trigger_type}")
            notification_manager.manage_notifications_for_object(
                origin_of_notification=appointment,
                trigger_type=trigger_type,
                group=appointment.group,
            )


@background(schedule=10)
def background_postponed_notifications():
    try:
        postponed_notifications()
    except Exception as e:
        import sentry_sdk

        logger.error(f"background_postponed_notifications {e}")
        sentry_sdk.capture_exception(e)
