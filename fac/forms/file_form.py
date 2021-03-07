# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from fac.models import File, Organization, Contact
from helpers.forms import JsonFileField


class OrganizationOrContact(forms.Field):
    # Validate a Organization or a Contact such as :
    #   {'pk': Organization.objects.last().pk, 'type': 'organisation'}
    #   {'pk': Contact.objects.last().pk, 'type': 'contact'}

    def _get_organization_instance(self, value):
        try:
            return Organization.objects.get(pk=value["pk"])
        except Organization.DoesNotExist:
            raise ValidationError("Invalid value [Organization.DoesNotExist]")

    def _get_contact_instance(self, value):
        try:
            return Contact.objects.get(pk=value["pk"])
        except Contact.DoesNotExist:
            raise ValidationError("Invalid value [Contact.DoesNotExist]")

    def clean(self, value):
        if value is None:
            if self.required:
                raise ValidationError("Required value")
            return None

        if value.get("type") == "contact":
            return self._get_contact_instance(value)
        elif value.get("type") == "organization":
            return self._get_organization_instance(value)

        raise ValidationError(f"Unknown value {value}")


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ("owning_group", "linked_object", "document", "url", "pinned", "note")

    linked_object = OrganizationOrContact()
    document = JsonFileField(required=False)

    def clean(self):
        super().clean()
        linked_object = self.cleaned_data.get("linked_object")
        owning_group_pk = self.cleaned_data.get("owning_group").pk

        if isinstance(linked_object, Contact):
            if owning_group_pk != linked_object.owning_group.pk:
                raise ValidationError("Le contact n'appartient pas à ce groupe")

        if isinstance(linked_object, Organization):
            if owning_group_pk != linked_object.owning_group.pk:
                raise ValidationError("La structure n'appartient pas à ce groupe")
        return self.cleaned_data

    def save(self, commit=True):
        file = super().save(commit=commit)
        file.linked_object = self.cleaned_data["linked_object"]
        file.save()

        return file
