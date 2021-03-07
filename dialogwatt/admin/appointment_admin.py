# -*- coding: utf-8 -*-
from django.contrib import admin

from dialogwatt.models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    base_model = Appointment
    list_display = [
        "pk",
        "uuid",
        "status",
        "subject",
        "start_date",
        "end_date",
        "sequence",
        "advisor",
        "content_type",
        "object_id",
        "place",
        "slot",
        "reason",
        "description",
        "has_been_honored",
    ]
    exclude = []
