# -*- coding: utf-8 -*-
from helpers.views import ApiView
from django.http import JsonResponse

from dialogwatt.helpers.find_slots import FindSlots

from rest_framework import status

from dialogwatt.models import Reason

from datetime import datetime


class FindAdvisorsForReasonView(ApiView):
    """
    find valid reasons for a given inseecode
    """

    def get(self, request, *args, **kwargs):
        try:
            reason = Reason.objects.get(pk=request.GET["reason"])
        except KeyError:
            return JsonResponse(
                {"Error": "Missing reason."}, status=status.HTTP_400_BAD_REQUEST
            )

        place = request.GET.get("place")

        start_date = datetime.today()

        fs = FindSlots(start_date=start_date, place=place, reason=reason)

        chunks = fs.find_free_time(duration=reason.duration)

        advisors = set()
        for i in chunks:
            for chunk in chunks[i]:
                if chunk["advisors"]:
                    for advisor in chunk["advisors"]:
                        advisors.add(advisor)

        return JsonResponse({"advisors": list(advisors)}, safe=False)
