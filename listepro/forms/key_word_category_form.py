# -*- coding: utf-8 -*-
from django import forms

from listepro.models import KeyWordCategory


class KeyWordCategoryForm(forms.ModelForm):
    class Meta:
        model = KeyWordCategory
        exclude = ["created_at", "updated_at"]
