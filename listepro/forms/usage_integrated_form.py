# -*- coding: utf-8 -*-
from django import forms

from listepro.models import UsageIntegrated


class UsageIntegratedForm(forms.ModelForm):
    class Meta:
        model = UsageIntegrated
        exclude = ["created_at", "updated_at"]
