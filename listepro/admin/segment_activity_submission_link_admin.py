# -*- coding: utf-8 -*-
from django.contrib import admin

from listepro.models import SegmentActivitySubMissionLink


@admin.register(SegmentActivitySubMissionLink)
class SegmentActivitySubMissionLinkAdmin(admin.ModelAdmin):
    base_model = SegmentActivitySubMissionLink
    list_display = [
        "pk",
        "segment",
        "activity",
        "sub_mission",
    ]
    exclude = []
