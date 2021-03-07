# -*- coding: utf-8 -*-
from django import forms

from helpers.forms import JsonFileField
from newsletters.models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ["created_at", "updated_at"]

    image = JsonFileField(required=False)
