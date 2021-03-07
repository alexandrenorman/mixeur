# -*- coding: utf-8 -*-
from django import forms

from listepro.models import Segment


class SegmentForm(forms.ModelForm):
    class Meta:
        model = Segment
        exclude = ["created_at", "updated_at"]
