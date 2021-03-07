# -*- coding: utf-8 -*-
from django import forms

from messaging.models import SmsAccount

from phonenumber_field.formfields import PhoneNumberField


class SmsAccountTestForm(forms.ModelForm):
    class Meta:
        model = SmsAccount
        exclude = ["created_at", "updated_at", "group"]

    test_phone = PhoneNumberField()
