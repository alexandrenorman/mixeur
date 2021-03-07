# -*- coding: utf-8 -*-
from django import forms

from experiences.models import SponsorTag


class SponsorTagForm(forms.ModelForm):
    class Meta:
        model = SponsorTag
        exclude = ["created_at", "updated_at"]
