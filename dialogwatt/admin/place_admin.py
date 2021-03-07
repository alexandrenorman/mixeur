# -*- coding: utf-8 -*-
from django.contrib import admin

from dialogwatt.models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    base_model = Place
    list_display = [
        "pk",
        "name",
        "color",
        "slug",
        "presentation",
        "internal_presentation",
        "is_active",
        "address",
        "city",
        "postcode",
        "lat",
        "lon",
        "inseecode",
        "url",
        "email",
        "phone",
    ]
    exclude = []
