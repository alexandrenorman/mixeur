# -*- coding: utf-8 -*-
from django.urls import resolve

from nested_admin import NestedStackedInline
from nested_admin.forms import SortableHiddenMixin

from .forms import ActionModelAdminForm
from ..models import ActionModel, Action


class ActionModelInlineMixin:
    model = ActionModel
    sortable_field_name = "order"
    form = ActionModelAdminForm
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        BaseFormSet = super().get_formset(request, obj, **kwargs)
        BaseFormSet.request = request

        class FormSet(BaseFormSet):
            def __init__(self, *args, **kwargs):
                form_kwargs = kwargs.pop("form_kwargs", {})
                pk_folder_model = resolve(request.path_info).kwargs.get("object_id")
                form_kwargs["folder_model"] = pk_folder_model
                super().__init__(*args, form_kwargs=form_kwargs, **kwargs)

            def save(self, commit=True):
                instance = super().save(commit=commit)
                for action_model in instance:
                    if not (
                        action_model.default
                        and action_model.should_generate_default_actions
                    ):
                        continue

                    # if the actions will be there by default AND we specified that
                    #   we want the actions to be added for existing folders
                    #   then:
                    folders = action_model.category_model.folder_model.folders.all()
                    for folder in folders:
                        valorization = action_model.valorizations.filter(
                            type_valorization=folder.type_valorization
                        ).first()
                        action, _ = Action.objects.get_or_create(
                            folder=folder, model=action_model, valorization=valorization
                        )
                return instance

        return FormSet


class ActionModelInlineAdmin(
    ActionModelInlineMixin, SortableHiddenMixin, NestedStackedInline
):

    fk_name = "category_model"
    verbose_name_plural = "Modèles d'actions"
