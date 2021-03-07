# -*- coding: utf-8 -*-
from django import forms

from listepro.models import Mission


class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        exclude = ["created_at", "updated_at"]
