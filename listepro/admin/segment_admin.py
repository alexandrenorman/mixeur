# -*- coding: utf-8 -*-
from django.contrib import admin

from listepro.models import Segment


@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    base_model = Segment
    list_display = [
        "pk",
        "name",
        "icon",
    ]
    exclude = []
