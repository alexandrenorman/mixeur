# -*- coding: utf-8 -*-
from django import forms

from listepro.models import SegmentActivitySubMissionLink


class SegmentActivitySubMissionLinkForm(forms.ModelForm):
    class Meta:
        model = SegmentActivitySubMissionLink
        exclude = ["created_at", "updated_at"]
