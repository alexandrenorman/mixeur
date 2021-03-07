# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from fac.models import Contact

from helpers.forms import SelectToCharField


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ["created_at", "updated_at", "tags", "referents"]

        civility = SelectToCharField()


class ContactListFilterForm(forms.ModelForm):
    filter = forms.CharField(label="Filtrer", max_length=80, required=True)  # NOQA
    sort_key = forms.CharField(label=_("Ordre"), max_length=80, required=True)

    class Meta:
        model = Contact
        fields = ("filter", "sort_key")


class DuplicateMergeForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = (
            "civility",
            "first_name",
            "last_name",
            "email",
            "address",
            "zipcode",
            "inseecode",
            "town",
            "lat",
            "lon",
            "country",
            "phone",
            "mobile_phone",
            "fax",
        )
