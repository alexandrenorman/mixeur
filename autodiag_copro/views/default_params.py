# -*- coding: utf-8 -*-
import json

from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from helpers.views import AdvisorRequiredApiView

from accounts.models import User
from autodiag_copro.models import DefaultParams, DefaultYearlyCombustibleParams

from autodiag_copro.forms import DefaultParamsForm

from autodiag_copro.serializers import (
    DefaultParamsSerializer,
    DefaultCombustibleParamsSerializer,
    DefaultYearlyCombustibleParamsSerializer,
)


class DefaultParamsView(AdvisorRequiredApiView):
    """
    ParamsView requires authenticated advisor

    get :model:`autodiag_copro.Params`

    """

    def get(self, request, *args, **kwargs):
        """
        Get :model:`autodiag_copro.DefaultParams` by [pk]
        """
        try:
            user_pk = kwargs["user_pk"]
        except KeyError:
            return JsonResponse(
                {"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        user = get_object_or_404(User, pk=user_pk, is_active=True)
        default_params = DefaultParams.default_value(key=user.group.pk)
        default_combustibles_params = default_params.combustible_params.all()
        ids = list(default_combustibles_params.values_list("id", flat=True))
        default_yearly_combustibles_params = DefaultYearlyCombustibleParams.objects.filter(
            combustible_params_id__in=ids
        )

        return JsonResponse(
            {
                "main_params": DefaultParamsSerializer(default_params).data,
                "combustibles_params": {
                    "combustibles_params": DefaultCombustibleParamsSerializer(
                        default_combustibles_params, many=True
                    ).data,
                    "yearly_combustibles_params": DefaultYearlyCombustibleParamsSerializer(
                        default_yearly_combustibles_params, many=True
                    ).data,
                },
            }
        )

    def patch(self, request, *args, **kwargs):
        """
        Update :model:`autodiag_copro.DefaultParams` by [pk]

        Must have default_params.change permission
        """
        try:
            key = kwargs["pk"]
        except KeyError:
            return JsonResponse(
                {"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        default_params_data = json.loads(request.body)

        pk = key
        default_params = get_object_or_404(DefaultParams, pk=pk)

        if not request.user.has_perm("default_params.change", default_params):
            return JsonResponse(
                {"error": "change not permitted"}, status=status.HTTP_403_FORBIDDEN
            )

        form = DefaultParamsForm(default_params_data, instance=default_params)
        if form.is_valid():
            form.save()
        else:
            return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

        return self.get(request)
