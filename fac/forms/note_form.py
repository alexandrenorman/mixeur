# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from fac.models import Note, Organization, Contact

from .reminder_form import ReminderFormMixin
from .organization_or_contact_field import OrganizationOrContactField


class NoteForm(ReminderFormMixin, forms.ModelForm):
    class Meta:
        model = Note
        fields = ("owning_group", "linked_object", "note", "pinned")

    linked_object = OrganizationOrContactField()

    def clean(self):
        super().clean()
        linked_object = self.cleaned_data.get("linked_object")
        owning_group_pk = self.cleaned_data.get("owning_group").pk

        if isinstance(linked_object, Contact):
            if owning_group_pk != linked_object.owning_group.pk:
                raise ValidationError(_("Le contact n'appartient pas à ce groupe"))

        if isinstance(linked_object, Organization):
            if owning_group_pk != linked_object.owning_group.pk:
                raise ValidationError(_("La structure n'appartient pas à ce groupe"))

        return self.cleaned_data

    def save(self, commit=True, *args, **kwargs):
        note = super().save(commit=commit)
        note.linked_object = self.cleaned_data["linked_object"]
        note.save()
        return note
