# -*- coding: utf-8 -*-
from django.contrib import admin

from listepro.models import KeyWord


@admin.register(KeyWord)
class KeyWordAdmin(admin.ModelAdmin):
    base_model = KeyWord
    list_display = [
        "pk",
        "name",
        "category",
    ]
    exclude = []
