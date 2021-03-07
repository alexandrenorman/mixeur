# -*- coding: utf-8 -*-
from django import forms

from messaging.models import TwilioAccount


class TwilioAccountForm(forms.ModelForm):
    class Meta:
        model = TwilioAccount
        exclude = ["created_at", "updated_at"]

    is_active = forms.BooleanField(required=False)
