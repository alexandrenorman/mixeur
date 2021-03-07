# -*- coding: utf-8 -*-
from datetime import timedelta


# ## CORS Framework config ##################################

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    # TODO - set this properly for production
    "http://127.0.0.1:8888",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8000",
)

# ## /CORS Framework config #################################


# ## REST Framework config ##################################

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        "helpers.drf_permission_backend.APrioriDjangoObjectPermissions",
        # By default we set everything to admin,
        #   then open endpoints on a case-by-case basis
        # 'rest_framework.permissions.IsAdminUser',
        # 'rest_framework.permissions.IsAuthenticated',
    ),
    "TEST_REQUEST_RENDERER_CLASSES": (
        "rest_framework.renderers.MultiPartRenderer",
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.TemplateHTMLRenderer",
    ),
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 20,
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'helpers.drf_permission_backend.APrioriDjangoObjectPermissions'
    # ],
    "DATE_INPUT_FORMATS": ["iso-8601", "%Y-%m-%d %H:%M"],
}

# ## /REST Framework config ##################################


# ## JWT Framework config ###################################

JWT_AUTH = {
    "JWT_ALLOW_REFRESH": True,
    "JWT_EXPIRATION_DELTA": timedelta(hours=48),
    "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=7),
}

# ## /JWT Framework config ##################################
