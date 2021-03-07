CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "default",
    },
    # Cache used when loading WhiteLabelling data from json/yaml files
    "wl_cdn_data": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "wl_cdn_data",
    },
}
