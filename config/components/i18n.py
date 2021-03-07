# -*- coding: utf-8 -*-


# ## I18N ##################################

# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = "fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = False  # True
USE_L10N = True
USE_TZ = True
LANGUAGES = (("fr", "fr"),)

PHONENUMBER_DB_FORMAT = "NATIONAL"
PHONENUMBER_DEFAULT_REGION = "FR"

CMS_LANGUAGES = {
    1: [
        {
            "redirect_on_fallback": True,
            "public": True,
            "hide_untranslated": False,
            "code": "fr",
            "name": "fr",
        }
    ],
    "default": {
        "redirect_on_fallback": True,
        "hide_untranslated": False,
        "public": True,
    },
}

# ## /I18N ##################################
