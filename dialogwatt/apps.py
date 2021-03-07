# -*- coding: utf-8 -*-

from django.apps import AppConfig

from core.helpers import is_jenkins_build, restart_background_task


class DialogwattAppConfig(AppConfig):
    name = "dialogwatt"

    def ready(self):
        if not is_jenkins_build():
            import dialogwatt.signals  # NOQA: F401

            import logging

            logger = logging.getLogger(__name__)  # NOQA
            logger.info("starting DialogWatt")

            from .tasks import (
                background_clean_unconfirmed_appointment,
                background_postponed_notifications,
            )

            restart_background_task(
                name="dialogwatt.tasks.background_clean_unconfirmed_appointment.background_clean_unconfirmed_appointment",  # NOQA: E501
                endpoint=background_clean_unconfirmed_appointment,
                repeat=5,
            )
            restart_background_task(
                name="dialogwatt.tasks.background_postponed_notifications.background_postponed_notifications",
                endpoint=background_postponed_notifications,
                repeat=5,
            )
