# -*- coding: utf-8 -*-
from fac.models import EcorenoverSimulation
from helpers.serializers import AutoModelSerializer


class EcorenoverSimulationSerializer(AutoModelSerializer):
    model = EcorenoverSimulation

    exclude = ["content_type", "object_id", "linked_object", "contact", "organization"]

    def get_owning_group(self, obj):
        return obj.owning_group.pk
