# -*- coding: utf-8 -*-
from django import forms


class AbstractTagForm(forms.ModelForm):
    class Meta:
        model = None
        exclude = ["created_at", "updated_at"]
