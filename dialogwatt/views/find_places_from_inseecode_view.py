# -*- coding: utf-8 -*-
from django.http import JsonResponse

from rest_framework import status

from dialogwatt.forms import FindPlacesFromInseecodeForm
from dialogwatt.models import CatchmentArea, Place, Slot
from dialogwatt.serializers import PlaceSerializer

from helpers.views import ApiView


class FindPlacesFromInseecodeView(ApiView):
    """
    find places from inseecode and reason
    """

    def get(self, request, *args, **kwargs):

        form = FindPlacesFromInseecodeForm(kwargs)
        if form.is_valid():
            catchment_areas = (
                CatchmentArea.objects.filter(territories=form.cleaned_data["inseecode"])
                .distinct()
                .values("id")
            )

            slots = Slot.active_and_future.filter(catchment_area__in=catchment_areas)
            slots = slots.filter(reasons__in=[form.cleaned_data["reason"]])

            slots_places = slots.values("place")

            places = Place.objects.filter(pk__in=slots_places)

            serializer = PlaceSerializer(places, many=True)
            return JsonResponse(serializer.data, safe=False)

        else:
            return JsonResponse(
                {"Error": form.errors}, status=status.HTTP_400_BAD_REQUEST
            )
