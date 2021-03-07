# -*- coding: utf-8 -*-
from django import forms

from messaging.models import SmsAccount


class SmsAccountForm(forms.ModelForm):
    class Meta:
        model = SmsAccount
        exclude = ["created_at", "updated_at"]

    is_active = forms.BooleanField(required=False)
