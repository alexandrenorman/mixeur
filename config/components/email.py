# -*- coding: utf-8 -*-
import environ
import logging

env = environ.Env()
logger = logging.getLogger(__name__)


# ## Email configuration ##################################
DJANGO_ANYMAIL_USE_MAILGUN = env.bool("DJANGO_ANYMAIL_USE_MAILGUN", default=False)

if DJANGO_ANYMAIL_USE_MAILGUN:
    logger.warning("----------------------------------")
    logger.warning("Starting MAILGUN support.")
    logger.warning("----------------------------------")
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

    INSTALLED_APPS += ["anymail"]  # NOQA: F821

    ANYMAIL = {
        "MAILGUN_API_KEY": env("DJANGO_MAILGUN_API_KEY", default=""),
        "MAILGUN_SENDER_DOMAIN": env("DJANGO_MAILGUN_SENDER_DOMAIN", default=""),
        "MAILGUN_WEBHOOK_SIGNING_KEY": env(
            "DJANGO_MAILGUN_WEBHOOK_SIGNING_KEY", default=""
        ),
        "MAILGUN_API_URL": env(
            "DJANGO_MAILGUN_API_URL", default="https://api.eu.mailgun.net/v3"
        ),
    }

else:
    logger.warning("----------------------------------")
    logger.warning("Starting vanilla SMTP support.")
    logger.warning("----------------------------------")
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = env("EMAIL_HOST", default="mail")
    EMAIL_PORT = env("EMAIL_PORT", default=1025)
    EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="docker")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
    EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=False)
    EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)


DEFAULT_FROM_EMAIL = env("DJANGO_DEFAULT_FROM_EMAIL")
DEFAULT_FROM_EMAIL_NAME = env("DJANGO_DEFAULT_FROM_EMAIL_NAME", default="")

# ## /Email configuration ##################################
