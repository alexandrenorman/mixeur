# -*- coding: utf-8 -*-
from django import forms

from listepro.models import Helper


class HelperForm(forms.ModelForm):
    class Meta:
        model = Helper
        exclude = ["created_at", "updated_at"]
