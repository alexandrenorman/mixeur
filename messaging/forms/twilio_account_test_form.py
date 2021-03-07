# -*- coding: utf-8 -*-
from django import forms

from messaging.models import TwilioAccount

from phonenumber_field.formfields import PhoneNumberField


class TwilioAccountTestForm(forms.ModelForm):
    class Meta:
        model = TwilioAccount
        exclude = ["created_at", "updated_at", "group"]

    test_phone = PhoneNumberField()
