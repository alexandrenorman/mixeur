# -*- coding: utf-8 -*-
from django.contrib import admin

from listepro.models import ProfessionalImage


@admin.register(ProfessionalImage)
class ProfessionalImageAdmin(admin.ModelAdmin):
    base_model = ProfessionalImage
    list_display = [
        "pk",
        "name",
        "cropped",
    ]
    exclude = []
