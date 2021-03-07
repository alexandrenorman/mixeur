# -*- coding: utf-8 -*-
from django import forms

from accounts.models import User


class ReferentsSearchForm(forms.Form):
    referents = forms.ModelMultipleChoiceField(queryset=User.advisors.all())
