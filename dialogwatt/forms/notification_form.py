# -*- coding: utf-8 -*-
from django import forms

from dialogwatt.models import Notification


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        exclude = ["created_at", "updated_at", "places", "reasons", "advisors"]

    all_places = forms.BooleanField(required=False)
    all_reasons = forms.BooleanField(required=False)

    is_active = forms.BooleanField(required=False)
    sms_is_active = forms.BooleanField(required=False)
    mail_is_active = forms.BooleanField(required=False)
    chat_is_active = forms.BooleanField(required=False)

    term_days = forms.IntegerField(required=False)
    term_day_type = forms.CharField(required=False)
    term_after_before = forms.CharField(required=False)
    term_time = forms.TimeField(required=False)

    # trigger = SelectToCharField()
    # term = SelectToCharField()
    # term_day_type = SelectToCharField(required=False)
    # term_after_before = SelectToCharField(required=False)
    # to = SelectToCharField()
