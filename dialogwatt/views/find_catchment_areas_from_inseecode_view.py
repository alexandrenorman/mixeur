# -*- coding: utf-8 -*-
from helpers.views import ApiView
from django.http import JsonResponse

from rest_framework import status

from dialogwatt.models import CatchmentArea
from dialogwatt.serializers import CatchmentAreaSerializer


class FindCatchmentAreasFromInseecodeView(ApiView):
    def get(self, request, *args, **kwargs):
        try:
            inseecode = kwargs["inseecode"]
        except KeyError:
            return JsonResponse(
                {"Error": "Missing inseecode"}, status=status.HTTP_400_BAD_REQUEST
            )

        catchment_areas = CatchmentArea.objects.filter(
            territories__inseecode=inseecode
        ).distinct()

        serializer = CatchmentAreaSerializer(catchment_areas, many=True)
        return JsonResponse(serializer.data, safe=False)
