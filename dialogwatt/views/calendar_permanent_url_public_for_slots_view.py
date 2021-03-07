# -*- coding: utf-8 -*-
from helpers.views import ApiView
from django.http import HttpResponse

from django.shortcuts import get_object_or_404

from django.db.models import Q

from dialogwatt.models import CalendarPermanentUrl, Slot
from dialogwatt.helpers import calendar_from_queryset


class CalendarPermanentUrlPublicForSlotsView(ApiView):
    """
    """

    def get(self, request, *args, **kwargs):
        """
        """
        uid = kwargs["unique_id"]
        calendar_permanent_url = get_object_or_404(CalendarPermanentUrl, unique_id=uid)

        qs = Slot.selectable.filter(group=calendar_permanent_url.user.group)

        if calendar_permanent_url.advisors.exists():
            qs = qs.filter(
                Q(advisors__in=calendar_permanent_url.advisors.all())
                | Q(use_advisor_calendar=False)
            )

        if calendar_permanent_url.places.exists():
            qs = qs.filter(place__in=calendar_permanent_url.places.all())

        if calendar_permanent_url.reasons.exists():
            qs = qs.filter(reasons__in=calendar_permanent_url.reasons.all())

        qs = qs.distinct()

        ical_out = calendar_from_queryset(qs)

        response = HttpResponse(ical_out, content_type="content-type:text/calendar")
        response["Content-Disposition"] = "attachment; filename=calendar.ics"

        return response
