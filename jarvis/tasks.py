# -*- coding: utf-8 -*-

import logging

from background_task import background

import sentry_sdk

logger = logging.getLogger(__name__)  # NOQA


def run_jarvis():
    from jarvis.jarvis import Jarvis

    logger.warning("Jarvis read its mailbox")
    jarvis = Jarvis()
    jarvis.read_mails()


@background(schedule=10)
def background_jarvis_read_your_mail():
    try:
        run_jarvis()
    except Exception as e:
        sentry_sdk.capture_exception(e)

    return
