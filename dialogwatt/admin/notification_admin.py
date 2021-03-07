# -*- coding: utf-8 -*-
from django.contrib import admin

from dialogwatt.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    base_model = Notification
    list_display = [
        "pk",
        "name",
        "group",
        "is_active",
        "trigger",
        "term",
        "term_days",
        "term_day_type",
        "term_after_before",
        "term_time",
        "all_reasons",
        "all_places",
        "to",
        "sms_is_active",
        "sms_message",
        "mail_is_active",
        "mail_subject",
        "mail_message",
        "chat_is_active",
        "chat_message",
    ]
    exclude = []
