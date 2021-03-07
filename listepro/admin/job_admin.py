# -*- coding: utf-8 -*-
from django.contrib import admin

from listepro.models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    base_model = Job
    list_display = [
        "pk",
        "name",
    ]
    exclude = []
