# -*- coding: utf-8 -*-
from django import forms

from visit_report.models import FinancialAid


class FinancialAidForm(forms.ModelForm):
    class Meta:
        model = FinancialAid
        exclude = ["created_at", "updated_at"]

    selected = forms.BooleanField(required=False)
