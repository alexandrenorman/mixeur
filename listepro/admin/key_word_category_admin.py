# -*- coding: utf-8 -*-
from django.contrib import admin

from listepro.models import KeyWordCategory


@admin.register(KeyWordCategory)
class KeyWordCategoryAdmin(admin.ModelAdmin):
    base_model = KeyWordCategory
    list_display = [
        "pk",
        "name",
    ]
    exclude = []
