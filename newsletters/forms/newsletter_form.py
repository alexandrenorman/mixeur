# -*- coding: utf-8 -*-
from django import forms
from helpers.forms import ISODateTimeField

from newsletters.models import Newsletter


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        exclude = ["created_at", "updated_at"]

    is_active = forms.BooleanField(required=False)

    is_public = forms.BooleanField(required=False)

    publication_start_date = ISODateTimeField(required=False)
    publication_end_date = ISODateTimeField(required=False)
