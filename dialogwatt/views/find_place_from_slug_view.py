# -*- coding: utf-8 -*-
from helpers.views import ApiView
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from types import SimpleNamespace

from rest_framework import status

from dialogwatt.models import Place, Reason
from dialogwatt.serializers import PlaceWithReasonsSerializer

from datetime import datetime


class FindPlaceFromSlugView(ApiView):
    """
    find a place from its slug
    """

    def get(self, request, *args, **kwargs):
        try:
            slug = kwargs["slug"]
        except KeyError:
            return JsonResponse(
                {"Error": "Missing slug"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            place = Place.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return JsonResponse(
                {"Error": "Lieu non trouvé"}, status=status.HTTP_404_NOT_FOUND
            )

        reasons = Reason.objects.filter(
            slot__place__pk=place.pk, slot__start_date__gt=datetime.now()
        ).distinct()

        place_with_reasons = SimpleNamespace()
        place_with_reasons.place = place
        place_with_reasons.reasons = reasons

        serializer = PlaceWithReasonsSerializer(place_with_reasons)
        return JsonResponse(serializer.data, safe=False)
