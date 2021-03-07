# -*- coding: utf-8 -*-
from django import forms
from helpers.forms import FullModelChoiceField

from experiences.models import ExperienceSponsor, SponsorTag


class ExperienceSponsorForm(forms.ModelForm):
    class Meta:
        model = ExperienceSponsor
        exclude = ["created_at", "updated_at"]

    sponsor = FullModelChoiceField(
        queryset=SponsorTag.objects.filter(is_active=True),
        required=True,
        to_field_name="pk",
    )
