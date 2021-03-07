# -*- coding: utf-8 -*-
from django import forms

from listepro.models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ["created_at", "updated_at"]
