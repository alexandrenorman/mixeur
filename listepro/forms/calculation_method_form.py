# -*- coding: utf-8 -*-
from django import forms

from listepro.models import CalculationMethod


class CalculationMethodForm(forms.ModelForm):
    class Meta:
        model = CalculationMethod
        exclude = ["created_at", "updated_at"]
