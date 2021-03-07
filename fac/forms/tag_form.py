# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from fac.models import Tag


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        exclude = ["created_at", "updated_at"]


class TagsListFilterForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("filter", "sort_key")

    filter = forms.CharField(label=_("Filtrer"), max_length=80, required=True)
    sort_key = forms.CharField(label=_("Ordre"), max_length=80, required=True)
