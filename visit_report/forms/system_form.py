# -*- coding: utf-8 -*-
from django import forms

from visit_report.models import System


class SystemForm(forms.ModelForm):
    class Meta:
        model = System
        exclude = ["created_at", "updated_at"]
