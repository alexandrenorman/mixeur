# -*- coding: utf-8 -*-
from django import forms

from visit_report.models import Scenario


class ScenarioForm(forms.ModelForm):
    class Meta:
        model = Scenario
        exclude = ["created_at", "updated_at"]
