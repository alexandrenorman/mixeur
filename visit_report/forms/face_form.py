# -*- coding: utf-8 -*-
from django import forms

from visit_report.models import Face


class FaceForm(forms.ModelForm):
    class Meta:
        model = Face
        exclude = ["created_at", "updated_at"]
