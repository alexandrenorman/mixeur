# -*- coding: utf-8 -*-
from django import forms

from messaging.models import SmtpAccount


class SmtpAccountTestForm(forms.ModelForm):
    class Meta:
        model = SmtpAccount
        exclude = ["created_at", "updated_at", "group"]

    test_email = forms.EmailField()
