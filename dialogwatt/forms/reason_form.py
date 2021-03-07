# -*- coding: utf-8 -*-
from django import forms

from dialogwatt.models import Reason


class ReasonForm(forms.ModelForm):
    class Meta:
        model = Reason
        exclude = ["created_at", "updated_at"]

    show_description = forms.BooleanField(required=False)
    color = forms.CharField(required=False)
