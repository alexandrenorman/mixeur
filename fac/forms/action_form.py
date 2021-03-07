# -*- coding: utf-8 -*-
from datetime import datetime

from django import forms
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from fac.models import Action, File

from helpers.forms import MultipleJsonFileField

from .reminder_form import ReminderFormMixin


class ActionForm(ReminderFormMixin, forms.ModelForm):
    documents = MultipleJsonFileField(required=False)

    def save(self, commit=True):
        instance = super().save(commit)
        for document in self.documents:
            File.objects.create(
                owning_group=instance.folder.owning_group,
                linked_object=instance,
                document=document,
            )
        return instance

    def clean(self):
        self.documents = self.cleaned_data.pop("documents", [])
        date = self.cleaned_data.get("date")
        if not date and self.cleaned_data.get("done"):
            self.cleaned_data["date"] = datetime.now()

        model = self.cleaned_data.get("model")

        if self.cleaned_data["done"]:
            if model.message_required and not strip_tags(self.cleaned_data["message"]):
                raise forms.ValidationError(
                    {"message": _("Le commentaire ne peut pas être vide.")}
                )

            files_linked = self.instance.files.all()
            if model.file_required and not self.documents and not files_linked:
                raise forms.ValidationError(
                    {"documents": _("Au moins une pièce jointe est requise.")}
                )

            if model.contact_required and not self.cleaned_data.get("contact"):
                raise forms.ValidationError(
                    {"contact": _("Il faut ajouter un contact lié.")}
                )

        super().clean()

    class Meta:
        model = Action
        fields = (
            "duration",
            "date",
            "done",
            "done_by",
            "message",
            "folder",
            "model",
            "contact",
            "valorization",
            "custom_form_data",
        )
