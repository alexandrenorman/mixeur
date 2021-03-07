# -*- coding: utf-8 -*-
from django.http import JsonResponse
from rest_framework import status

from helpers.views import ExpertRequiredApiView, ModelView

from experiences.models import Explanation
from experiences.forms import ExplanationForm
from experiences.serializers import ExplanationSerializer


class ExplanationView(ModelView, ExpertRequiredApiView):
    """
    Explanation View
    """

    model = Explanation
    form = ExplanationForm
    serializer = ExplanationSerializer
    perm_module = "experiences/explanation"
    updated_at_attribute_name = "updated_at"

    def get(self, request, *args, **kwargs):
        """
        """
        try:
            object = self.model.objects.get(owning_group=request.user.group)
        except self.model.DoesNotExist:

            return JsonResponse(None, safe=False)

        perm = self.get_perm_module(request, "GET")
        if perm and not request.user.has_perm(f"{perm}.view", object):
            return JsonResponse(
                {"error": "view not permitted"}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(request, "GET")(object)
        return JsonResponse(serializer.data)

    def pre_form(self, request, instance_data, created=False, *args, **kwargs):
        """
        pre_form operation

        can change instance_data before submiting to form

        created: True if object is created, False if updated
        """
        instance_data["owning_group"] = request.user.group.pk
        return instance_data
