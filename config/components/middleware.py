# -*- coding: utf-8 -*-

# ## Middleware ##################################

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "helpers.middleware.TransformPropertiesCaseMiddleware",
    "helpers.middleware.AddVersionNumberMiddleware",
]


# ## /Middleware ##################################
