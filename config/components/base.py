# -*- coding: utf-8 -*-

import os

import environ


env = environ.Env()

CSRF_COOKIE_NAME = "csrftoken"

# ## PATH ##################################

DATA_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE_NAME = env("SITE_NAME", default="mixeur")
APP_VERSION = env("APP_VERSION", default="undefined")
SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["127.0.0.1"])

# ## /PATH ##################################


# ## Application definition ##################################

AUTH_USER_MODEL = "accounts.User"
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "core.wsgi.application"
APPEND_SLASH = True


LOGIN_REDIRECT_URL = "fac:contact_main"
LOGIN_URL = env("LOGIN_URL", default="/user/login/")


# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = "slugify.slugify"

# ## /Application definition ##################################


# ## static and media ##################################

# Static and media files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(DATA_DIR, "media")
STATIC_ROOT = os.path.join(DATA_DIR, "static")

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)
SITE_ID = 1

# ## /static and media ##################################


AUTHENTICATION_BACKENDS = (
    "simple_perms.PermissionBackend",
    "django.contrib.auth.backends.ModelBackend",
)

SIMPLE_PERMS_GLOBAL_DEFAULT_PERMISSION = "helpers.perms.global_default_permission"

DATA_UPLOAD_MAX_MEMORY_SIZE = 26214400

# Used to disable traefik configuration generation for some tests
SKIP_TRAEFIK_AUTOCONFIG_ON_WL_SAVE = False
