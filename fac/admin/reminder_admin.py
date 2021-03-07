# -*- coding: utf-8 -*-
from django.contrib import admin

from fac.models import Reminder


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "owning_group",
        "creator",
        "content_type_task",
        "object_id_task",
        "date",
        "done",
    ]
    exclude = []
