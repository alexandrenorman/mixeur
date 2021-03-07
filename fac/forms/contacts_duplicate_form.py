# -*- coding: utf-8 -*-
from django import forms

from fac.models import ContactsDuplicate


class ContactsDuplicateForm(forms.ModelForm):
    class Meta:
        model = ContactsDuplicate
        exclude = ["created_at", "updated_at"]

    acknowledged = forms.BooleanField(required=False)
