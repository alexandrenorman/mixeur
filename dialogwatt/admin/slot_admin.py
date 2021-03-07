# -*- coding: utf-8 -*-
from django.contrib import admin

from dialogwatt.models import Slot


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    base_model = Slot
    list_display = [
        "pk",
        "uuid",
        "status",
        "sequence",
        "text",
        "group",
        "start_date",
        "end_date",
        "visibility",
        "place",
        "catchment_area",
        "deadline",
        "time_between_slots",
        "use_advisor_calendar",
        "number_of_active_advisors",
        "description",
        "public_description",
    ]
    exclude = []
