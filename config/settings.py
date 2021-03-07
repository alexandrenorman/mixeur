# -*- coding: utf-8 -*-
"""
Django settings for djcms project.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

from split_settings.tools import include, optional

include(
    "components/base.py",
    "components/logging.py",
    "components/applications.py",
    "components/middleware.py",
    "components/debug.py",
    "components/sentry.py",
    "components/database.py",
    "components/email.py",
    "components/i18n.py",
    "components/rest_framework.py",
    "components/templates.py",
    "components/ckeditor.py",
    "components/caches.py",
    "components/jarvis.py",
    # "components/silk.py",  # Uncomment to enable silk profiler
    optional("local_settings.py"),
)
