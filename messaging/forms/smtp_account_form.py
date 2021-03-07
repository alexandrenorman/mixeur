# -*- coding: utf-8 -*-
from django import forms

from messaging.models import SmtpAccount


class SmtpAccountForm(forms.ModelForm):
    class Meta:
        model = SmtpAccount
        exclude = ["created_at", "updated_at"]

    is_active = forms.BooleanField(required=False)

    email_use_tls = forms.BooleanField(required=False)

    email_use_ssl = forms.BooleanField(required=False)
