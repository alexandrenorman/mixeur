# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Debug


class DebugAdmin(admin.ModelAdmin):
    list_display = ["pk", "creation_date", "level", "sender", "message"]
    list_filter = ("level", "sender")
    search_fields = ("level", "sender", "message")
    exclude = []


admin.site.register(Debug, DebugAdmin)
