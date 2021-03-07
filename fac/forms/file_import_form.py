# -*- coding: utf-8 -*-
from django import forms

from fac.models import FileImport


class FileImportForm(forms.ModelForm):
    class Meta:
        model = FileImport
        exclude = ["created_at", "updated_at"]
