# -*- coding: utf-8 -*-
from django import forms

from visit_report.models import Appendix


class AppendixForm(forms.ModelForm):
    class Meta:
        model = Appendix
        exclude = ["created_at", "updated_at"]

    selected = forms.BooleanField(required=False)
