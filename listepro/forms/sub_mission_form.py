# -*- coding: utf-8 -*-
from django import forms

from listepro.models import SubMission


class SubMissionForm(forms.ModelForm):
    class Meta:
        model = SubMission
        exclude = ["created_at", "updated_at"]
