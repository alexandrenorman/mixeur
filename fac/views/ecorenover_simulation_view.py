# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType

from fac.forms import EcorenoverSimulationForm
from fac.models import EcorenoverSimulation
from fac.serializers import EcorenoverSimulationSerializer
from helpers.views import ExpertRequiredApiView, ModelView


class EcorenoverSimulationView(ModelView, ExpertRequiredApiView):
    """
    EcorenoverSimulation View
    """

    model = EcorenoverSimulation
    form = EcorenoverSimulationForm
    serializer = EcorenoverSimulationSerializer
    perm_module = "ecorenover_simulation"

    def filter(self, request, queryset):
        file_type = request.GET.get("linkedObjectType")
        object_id = request.GET.get("objectId")
        if not file_type or not object_id:
            return queryset

        if file_type != "contact" and file_type != "organization":
            return queryset

        content_type = ContentType.objects.get(app_label="fac", model=file_type)
        return queryset.filter(object_id=object_id, content_type=content_type)
