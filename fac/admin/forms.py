from django import forms
from django.utils.translation import ugettext_lazy as _

from accounts.models import Group

from fac.models import FolderModel, Project

from ..models import ActionModel, Status, Valorization


class ActionModelAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        folder_model_pk = kwargs.pop("folder_model")
        super().__init__(*args, **kwargs)
        self.fields["trigger_status"].queryset = Status.objects.none()
        self.fields["valorizations"].queryset = Valorization.objects.none()
        if folder_model_pk:
            folder_model = FolderModel.objects.get(pk=folder_model_pk)
            status_queryset = Status.objects.filter(folder_model=folder_model_pk)

            valorizations_queryset = Valorization.objects.filter(
                type_valorization__in=folder_model.project.type_valorizations.all()
            )
            self.fields["trigger_status"].queryset = status_queryset
            self.fields["valorizations"].queryset = valorizations_queryset

    def clean(self):
        if not self.cleaned_data["default"] and not self.cleaned_data["optional"]:
            raise forms.ValidationError(
                _("Le modèle d'action doit au minimum être 'optionnel' ou 'défaut'.")
            )
        return super().clean()

    class Meta:
        model = ActionModel
        exclude = []
        help_texts = {
            "trigger_status": _(
                "Pour selectionner un status, il faut au préalable renseigner "
                "des status au modèle de dossier courant."
            ),
            "valorizations": _(
                "Pour selectionner des valorisations, il faut au préalable "
                "associer des types de valorisation au projet lié au modèle de dossier "
                "courant.<br>"
            ),
        }


class ProjectAdminForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.order_by("name"), required=False
    )

    def clean_type_valorizations(self):
        """ 1 Group = 1 TypeValorization for 1 FolderModel  """
        cleaned_data = super().clean()
        type_valorizations = cleaned_data["type_valorizations"]
        if type_valorizations:
            groups = [
                group
                for type_valorization in type_valorizations
                for group in type_valorization.groups.all()
            ]
            set_groups = set(groups)
            if len(groups) != len(set_groups):
                raise forms.ValidationError(
                    _(
                        "Vous ne pouvez pas associer plusieurs types de "
                        "valorisation appartenant au même groupe."
                    )
                )
        return type_valorizations

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("type_valorizations") and cleaned_data.get("groups"):
            type_valorization_groups = {
                group.pk
                for type_valorization in cleaned_data.get("type_valorizations")
                for group in type_valorization.groups.all()
            }
            groups = {group.pk for group in cleaned_data.get("groups")}
            if groups != type_valorization_groups:
                raise forms.ValidationError(
                    _(
                        "Les groupes sélectionnés, ne correspondent pas aux "
                        "groupes des types de valorisation. Videz les groupes "
                        "pour éviter les conflits."
                    )
                )

    def save(self, commit=True):
        type_valorizations = self.cleaned_data["type_valorizations"]
        if type_valorizations:
            self.cleaned_data["groups"] = Group.objects.filter(
                type_valorizations__in=type_valorizations
            )
        return super().save(commit=commit)

    class Meta:
        model = Project
        exclude = []
