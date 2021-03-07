# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.conf import settings

from core.helpers import (
    delete_background_task,
    is_jenkins_build,
    restart_background_task,
)


class JarvisAppConfig(AppConfig):
    name = "jarvis"
    TASK_NAME = "jarvis.tasks.background_jarvis_read_your_mail"

    def ready(self):
        if not is_jenkins_build():
            if settings.JARVIS_EMAIL:
                from .tasks import background_jarvis_read_your_mail

                import logging

                logger = logging.getLogger(__name__)  # NOQA

                restart_background_task(
                    name=self.TASK_NAME,
                    endpoint=background_jarvis_read_your_mail,
                    repeat=15,
                )
            else:
                delete_background_task(name=self.TASK_NAME)
