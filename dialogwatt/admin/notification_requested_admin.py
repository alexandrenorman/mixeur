# -*- coding: utf-8 -*-
from django.contrib import admin

from dialogwatt.models import NotificationRequested


@admin.register(NotificationRequested)
class NotificationRequestedAdmin(admin.ModelAdmin):
    base_model = NotificationRequested
    list_display = ["pk", "notification", "exchange", "content_type", "object_id"]
    exclude = []
