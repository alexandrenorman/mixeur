# -*- coding: utf-8 -*-
from django import forms

from fac.models import RgpdConsentForContacts


class RgpdConsentForContactsForm(forms.ModelForm):
    class Meta:
        model = RgpdConsentForContacts
        fields = (
            "contact",
            "allow_to_keep_data",
            "allow_to_use_phone_number_to_send_reminder",
            "allow_to_use_email_to_send_reminder",
            "allow_to_share_my_information_with_my_advisor",
            "allow_to_share_my_information_with_partners",
        )
