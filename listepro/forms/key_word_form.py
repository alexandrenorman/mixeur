# -*- coding: utf-8 -*-
from django import forms

from listepro.models import KeyWord


class KeyWordForm(forms.ModelForm):
    class Meta:
        model = KeyWord
        exclude = ["created_at", "updated_at"]
