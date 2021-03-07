# -*- coding: utf-8 -*-
import sys

import environ

# ## Logging ##################################
env = environ.Env()

# doublon with debug… but we need to enable logging before
DEBUG = env.bool("DJANGO_DEBUG", default=False)
logging_level = "DEBUG" if DEBUG else "INFO"
module_logging_level = "DEBUG" if DEBUG else "INFO"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "timestamp": {
            "format": "{asctime} {levelname} {message}",  # NOQA: FS003
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": logging_level,
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "timestamp",
        }
    },
    "loggers": {
        "django": {"level": "ERROR", "handlers": ["console"]},
        "accounts": {"level": module_logging_level, "handlers": ["console"]},
        "actimmo_map": {"level": module_logging_level, "handlers": ["console"]},
        "autodiag_copro": {"level": module_logging_level, "handlers": ["console"]},
        "ckeditor_custom": {"level": module_logging_level, "handlers": ["console"]},
        "config": {"level": module_logging_level, "handlers": ["console"]},
        "core": {"level": module_logging_level, "handlers": ["console"]},
        "custom_forms": {"level": module_logging_level, "handlers": ["console"]},
        "dialogwatt": {"level": module_logging_level, "handlers": ["console"]},
        "ecorenover": {"level": module_logging_level, "handlers": ["console"]},
        "energies": {"level": module_logging_level, "handlers": ["console"]},
        "experiences": {"level": module_logging_level, "handlers": ["console"]},
        "fac": {"level": module_logging_level, "handlers": ["console"]},
        "helpers": {"level": module_logging_level, "handlers": ["console"]},
        "jarvis": {"level": module_logging_level, "handlers": ["console"]},
        "listepro": {"level": module_logging_level, "handlers": ["console"]},
        "media": {"level": module_logging_level, "handlers": ["console"]},
        "messaging": {"level": module_logging_level, "handlers": ["console"]},
        "newsletters": {"level": module_logging_level, "handlers": ["console"]},
        "pdf_generator": {"level": module_logging_level, "handlers": ["console"]},
        "territories": {"level": module_logging_level, "handlers": ["console"]},
        "thermix": {"level": module_logging_level, "handlers": ["console"]},
        "visit_report": {"level": module_logging_level, "handlers": ["console"]},
        "white_labelling": {"level": module_logging_level, "handlers": ["console"]},
    },
}

# ## /Logging ##################################
