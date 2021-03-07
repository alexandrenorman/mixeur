# -*- coding: utf-8 -*-
from django import forms

from listepro.models import Activity


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        exclude = ["created_at", "updated_at"]
