# -*- coding: utf-8 -*-
from django.contrib import admin

from dialogwatt.models import Exchange


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    base_model = Exchange
    list_display = [
        "pk",
        "schedule",
        # "background_task",
        "from_account",
        # "to_account",
        "trigger",
        "subject",
        "message_sms_short",
        "message_mail_ascii_short",
        # "message_mail_html",
        "message_type",
        "has_been_sent_on",
        "has_been_received_on",
        "has_been_opened_on",
        "error",
    ]
    list_filter = ("trigger", "message_type")
    exclude = []

    def message_mail_ascii_short(self, obj):
        return obj.message_mail_ascii[:50]

    message_mail_ascii_short.short_description = "message mail ascii"

    def message_sms_short(self, obj):
        return obj.message_sms[:20]

    message_sms_short.short_description = "message sms"
