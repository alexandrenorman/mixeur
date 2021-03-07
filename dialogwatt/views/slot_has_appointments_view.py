# -*- coding: utf-8 -*-
from django.http import JsonResponse

from rest_framework import status

from dialogwatt.models import Slot

from helpers.views import ExpertRequiredApiView


class SlotHasAppointmentsView(ExpertRequiredApiView):
    def get(self, request, *args, **kwargs):
        """"""
        try:
            pk = kwargs["pk"]
        except KeyError:
            return JsonResponse(
                {"Error": "Missing PK"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            obj = Slot.objects.get(pk=pk)
        except Slot.DoesNotExist:
            return JsonResponse(
                {"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        return JsonResponse({"status": obj.has_appointments})
