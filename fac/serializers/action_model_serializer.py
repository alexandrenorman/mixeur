# -*- coding: utf-8 -*-
import serpy

from fac.models import ActionModel
from helpers.serializers import AutoModelSerializer


class ActionModelSerializer(AutoModelSerializer):
    model = ActionModel

    exclude = ["category_model"]

    category = serpy.MethodField()

    def get_category(self, obj):
        return obj.category_model.pk

    def get_trigger_status(self, obj):
        if obj.trigger_status:
            return obj.trigger_status.pk
        return ""

    def get_valorizations(self, obj):
        return [
            {"label": valorization.type_valorization.name, "value": valorization.pk}
            for valorization in obj.valorizations.all()
        ]
