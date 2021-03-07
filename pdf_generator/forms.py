# -*- coding: utf-8 -*-
from django import forms

from .models import PdfTempStore


class PdfTempStoreForm(forms.ModelForm):
    class Meta:
        model = PdfTempStore
        fields = ("data",)
