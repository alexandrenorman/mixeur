# -*- coding: utf-8 -*-
from django import forms

from visit_report.models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        exclude = ["created_at", "updated_at"]
