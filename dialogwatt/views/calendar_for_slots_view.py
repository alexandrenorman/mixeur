# -*- coding: utf-8 -*-
# from django.shortcuts import get_object_or_404
from helpers.views import AdvisorRequiredApiView
from django.http import HttpResponse

from dialogwatt.models import Slot
from dialogwatt.helpers import calendar_from_queryset

import json


# from django.core.exceptions import ValidationError
# from accounts.models import User


class CalendarForSlotsView(AdvisorRequiredApiView):
    """
    CalendarForSlotsView requires advisor user
    """

    def get(self, request, *args, **kwargs):
        """
        """
        # Only active slots
        qs = Slot.active.filter(group=request.user.group)

        if "advisors" in request.GET:
            advisors = json.loads(request.GET["advisors"])
            qs = qs.filter(advisors__in=advisors)

        if "places" in request.GET:
            places = json.loads(request.GET["places"])
            qs = qs.filter(place__in=places)

        if "reasons" in request.GET:
            reasons = json.loads(request.GET["reasons"])
            qs = qs.filter(reasons__in=reasons)

        qs = qs.distinct()

        ical_out = calendar_from_queryset(qs)

        response = HttpResponse(ical_out, content_type="content-type:text/calendar")
        response["Content-Disposition"] = "attachment; filename=calendar-crenaux.ics"

        return response
