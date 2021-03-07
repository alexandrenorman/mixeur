# -*- coding: utf-8 -*-
from django import forms

from helpers.forms import JsonFileField, FullModelChoiceField

from experiences.models import Experience

from accounts.models import User


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = [
            "created_at",
            "updated_at",
            "tags",
            "assignments",
            "sponsors",
            "jobs",
            "partners",
            "publics",
            "years",
        ]

    referent = FullModelChoiceField(
        queryset=User.objects.all(), required=True, to_field_name="pk"
    )
    image1 = JsonFileField(required=False)
    image2 = JsonFileField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        for partner in self.data["partners"]:
            if "is_european" in partner and partner["is_european"] is True:
                if (
                    cleaned_data["description_en"] == ""
                    or cleaned_data["description_en"] == "<p></p>"
                ):
                    raise forms.ValidationError(
                        "Un projet avec un partenaire européen doit comporter une description en anglais."
                    )
