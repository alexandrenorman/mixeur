# -*- coding: utf-8 -*-
from django import forms
from fac.models import ObjectiveAction, ActionModel


class ObjectiveActionsAdminForm(forms.ModelForm):
    class Meta:
        model = ObjectiveAction
        exclude = []

    model_action = forms.ModelChoiceField(
        queryset=ActionModel.objects.order_by(
            "category_model__folder_model__name", "order"
        )
    )
