# -*- coding: utf-8 -*-
import environ
import logging
import os

env = environ.Env()

logger = logging.getLogger(__name__)


# ## SENTRY  ##################################

SENTRY_KEY = env("SENTRY_KEY", default=None)
SENTRY_PROJECT = env("SENTRY_PROJECT", default=None)
SENTRY_HOST = env("SENTRY_HOST", default="sentry.hespul.org")

if SENTRY_KEY and SENTRY_PROJECT and SENTRY_HOST and not DEBUG:  # NOQA
    logger.warning("----------------------------------")
    logger.warning("Adding Sentry support.")
    logger.warning("----------------------------------")

    import sentry_sdk
    from sentry_sdk import configure_scope
    from sentry_sdk.integrations.django import DjangoIntegration

    APP_VERSION = env("APP_VERSION", default="unknown")
    # INSTANCE = env("DJANGO_SITE_URL", default="unknown")

    with configure_scope() as scope:
        for k in ("DJANGO_MIGRATE", "DJANGO_COLLECTSTATIC", "CONTAINER_NAME"):
            scope.set_extra(k, os.environ.get(k))

    sentry_sdk.init(
        dsn=f"https://{SENTRY_KEY}@{SENTRY_HOST}/{SENTRY_PROJECT}",
        integrations=[DjangoIntegration()],
        # send_default_pii=True, # Associate users to errors
        release=APP_VERSION,
        # server_name=INSTANCE,
        environment=env("APP_ENV", default="PROD"),
        with_locals=True,
    )
else:
    logger.warning("----------------------------------")
    logger.warning("Sentry not enabled")
    logger.warning("----------------------------------")

# ## /SENTRY  ##################################
