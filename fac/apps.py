# -*- coding: utf-8 -*-

from django.apps import AppConfig

from core.helpers import is_jenkins_build


class FacAppConfig(AppConfig):
    name = "fac"

    def ready(self):
        if not is_jenkins_build():
            import fac.signals  # NOQA: F401

            import logging

            logger = logging.getLogger(__name__)  # NOQA
            logger.info("starting Fac")
