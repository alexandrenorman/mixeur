# -*- coding: utf-8 -*-
from django.contrib import admin

from listepro.models import Professional


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    base_model = Professional
    list_display = [
        "pk",
        "name",
        "adress",
        "town",
        "postcode",
        "email",
        "url",
        "logo",
        "original_logo",
        "job",
        "activity_first",
        "activity_second",
        "activity_third",
        "activity_fourth",
        "personnal_key_words",
        "user",
        "is_in_progress",
        "pro_is_valid",
        "phone_number",
    ]
    exclude = []
