# -*- coding: utf-8 -*-
import logging

import environ

logger = logging.getLogger(__name__)


env = environ.Env()

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = env.bool("DJANGO_DEBUG", default=False)
PROFILER = env.bool("DJANGO_PROFILER", False)

# Override SMTP and SMS configuration to force using SMTP and SMS over SMTP
# for debugging purpose
OVERRIDE_SMTP_AND_SMS = env.bool("DJANGO_OVERRIDE_SMTP_AND_SMS", False)

# ## DEBUG  ##################################

print("----------------------------------")
if DEBUG:
    print("Activate DEBUG mode")
    SHELL_PLUS_PRINT_SQL = True
    SHELL_PLUS_SQLPARSE_FORMAT_KWARGS = dict(
        reindent_aligned=True, truncate_strings=500
    )
    SHELL_PLUS = "ipython"
    SHELL_PLUS_POST_IMPORTS = [("decimal", "Decimal"), ("accounts.models", "Group")]

    MIDDLEWARE += [  # NOQA: F821,E501
        "querycount.middleware.QueryCountMiddleware",
        "django.contrib.admindocs.middleware.XViewMiddleware",
    ]
    QUERYCOUNT = {"DISPLAY_DUPLICATES": 5}

    AUTHENTICATION_BACKENDS = (
        "simple_perms.PermissionBackend",
        "core.debug_auth_backend.DebugAuthBackend",
    )
else:
    print("No activation of DEBUG mode")

if PROFILER:
    logger.debug("Activate PROFILER: customizable-django-profiler")
    # https://github.com/someshchaturvedi/customizable-django-profiler
    MIDDLEWARE += ["customizable_django_profiler.cProfileMiddleware"]  # NOQA: F821,E501
    PROFILER = {"activate": True}

# ## /DEBUG  ##################################
