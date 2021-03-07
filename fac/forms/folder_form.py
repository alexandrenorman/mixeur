# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from fac.models import Folder, Contact, Organization


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


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ("owning_group", "linked_object", "description", "model")

    linked_object = OrganizationOrContact()

    def clean(self):
        cleaned_data = super().clean()

        if "model" not in cleaned_data:
            raise ValidationError(
                {
                    "model": _(
                        "Impossible d'enregistrer ce type de dossier pour un contact."
                    )
                }
            )

        linked_object_type = self["linked_object"].data["type"]
        if (
            linked_object_type == "contact"
            and not cleaned_data["model"].link_to_contact
        ):
            raise ValidationError(
                _("Impossible d'enregistrer ce type de dossier pour un contact.")
            )
        elif (
            linked_object_type == "organization"
            and not cleaned_data["model"].link_to_organization
        ):
            raise ValidationError(
                _("Impossible d'enregistrer ce type de dossier pour une structure.")
            )

    def save(self, commit=True):
        folder = super().save(commit=commit)
        folder.linked_object = self.cleaned_data["linked_object"]

        folder.save()

        return folder
