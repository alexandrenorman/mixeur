# -*- coding: utf-8 -*-
from django import forms

from visit_report.models import Financing


class FinancingForm(forms.ModelForm):
    class Meta:
        model = Financing
        exclude = ["created_at", "updated_at"]

    selected = forms.BooleanField(required=False)
