# -*- coding: utf-8 -*-
from django import forms

from fac.models import Project


class ProjectSearchForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all())
