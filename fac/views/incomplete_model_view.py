# -*- coding: utf-8 -*-
from django.http import JsonResponse

from fac.models import IncompleteModel
from fac.serializers import IncompleteModelSerializer

from helpers.views import ExpertRequiredApiView, ModelReadOnlyView


class IncompleteModelView(ModelReadOnlyView, ExpertRequiredApiView):
    """
    ContactsDuplicate View
    """

    model = IncompleteModel
    serializer = IncompleteModelSerializer
    perm_module = "fac/incomplete_model"

    def detail(self, request, *args, **kwargs):
        has_incomplete_models = IncompleteModel.objects.accessible_by(
            request.user
        ).exists()
        return JsonResponse(
            {
                "has_incomplete_models": has_incomplete_models,
            }
        )
