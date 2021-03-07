# -*- coding: utf-8 -*-
from django import forms


class updatedAtForm(forms.Form):
    updated_at = forms.FloatField(required=True)


class SearchForm(forms.Form):
    q = forms.CharField(max_length=100)
