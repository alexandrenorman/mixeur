# -*- coding: utf-8 -*-
from helpers.views import ApiView
from django.http import JsonResponse
from django.db.models import Prefetch

from rest_framework import status

from dialogwatt.models import Reason
from dialogwatt.serializers import FindReasonsSerializer

from datetime import datetime
from accounts.models import Group


class FindReasonsFromInseecodeView(ApiView):
    """
    find valid reasons for a given inseecode
    """

    def get(self, request, *args, **kwargs):
        try:
            inseecode = kwargs["inseecode"]
        except KeyError:
            return JsonResponse(
                {"Error": "Missing INSEECODE"}, status=status.HTTP_400_BAD_REQUEST
            )

        reasons = (
            Reason.objects.filter(
                slot__start_date__date__gte=datetime.today(),
                slot__catchment_area__territories__inseecode=inseecode,
            )
            .prefetch_related(
                Prefetch("group", queryset=Group.objects.only("pk").all())
            )
            .distinct()
        )

        if len(reasons) == 0:
            return JsonResponse(
                {
                    "Error": "Il n'y a pas de service proposé actuellement pour cette commune."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = FindReasonsSerializer(reasons, many=True)
        return JsonResponse(serializer.data, safe=False)
