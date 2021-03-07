# -*- coding: utf-8 -*-

from custom_forms.models import CustomForm

from helpers.serializers import (
    AutoModelSerializer,
)


class CustomFormSerializer(AutoModelSerializer):
    model = CustomForm
    exclude = [
        "action_models",
        "folder_models",
        "groups",
        "projects",
    ]

    def get_action_models(self, obj):
        return [x.pk for x in obj.action_models.all()]

    def get_folder_models(self, obj):
        return [x.pk for x in obj.folder_models.all()]

    def get_groups(self, obj):
        return [x.pk for x in obj.groups.all()]

    def get_projects(self, obj):
        return [x.pk for x in obj.projects.all()]
