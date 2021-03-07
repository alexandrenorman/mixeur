# -*- coding: utf-8 -*-
import serpy

from fac.models import Folder

from helpers.serializers import AutoModelSerializer

from .action_simple_serializer import ActionSimpleSerializer
from .folder_model_serializer import FolderModelSerializer
from .status_simple_serializer import StatusSimpleSerializer


class FolderSerializer(AutoModelSerializer):
    model = Folder
    exclude = ["content_type", "object_id", "linked_object", "contact", "organization"]

    status = serpy.MethodField()

    def get_custom_form_data(self, obj):
        if obj.custom_form_data is None:
            return {}

        return obj.custom_form_data

    def get_model(self, folder):
        return FolderModelSerializer(folder.model).data

    def get_actions(self, folder):
        actions = {}
        for action in folder.actions.all():
            category_pk = action.model.category_model.pk
            actions[category_pk] = actions.get(category_pk, []) + [
                ActionSimpleSerializer(action).data
            ]
        return actions

    def get_owning_group(self, folder):
        return folder.owning_group.pk

    def get_type_valorization(self, folder):
        if folder.type_valorization:
            return folder.type_valorization.pk

    def get_status(self, folder):
        status = folder.get_status()
        if status:
            return StatusSimpleSerializer(status).data
        return None
