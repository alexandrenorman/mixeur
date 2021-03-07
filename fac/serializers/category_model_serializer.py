# -*- coding: utf-8 -*-
import serpy

from fac.models import CategoryModel
from helpers.serializers import AutoModelSerializer

from .action_model_serializer import ActionModelSerializer


class CategoryModelSerializer(AutoModelSerializer):
    model = CategoryModel

    default_actions = serpy.MethodField()
    optional_actions = serpy.MethodField()

    def get_folder_model(self, obj):
        return obj.folder_model.pk

    def get_default_actions(self, obj):
        return [
            ActionModelSerializer(action_model).data
            for action_model in obj.action_models.all()
            if action_model.default
        ]

    def get_optional_actions(self, obj):
        return [
            ActionModelSerializer(action_model).data
            for action_model in obj.action_models.all()
            if action_model.optional
        ]
