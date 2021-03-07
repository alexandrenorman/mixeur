# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from dialogwatt.helpers import calendar_from_queryset
from dialogwatt.models import Appointment, CalendarPermanentUrl

from helpers.views import ApiView


class CalendarPermanentUrlPublicView(ApiView):
    """"""

    def get(self, request, *args, **kwargs):
        """"""
        uid = kwargs["unique_id"]
        calendar_permanent_url = get_object_or_404(CalendarPermanentUrl, unique_id=uid)

        qs = Appointment.active.filter(slot__group=calendar_permanent_url.user.group)

        if calendar_permanent_url.advisors.exists():
            qs = qs.filter(advisor__in=calendar_permanent_url.advisors.all())

        if calendar_permanent_url.places.exists():
            qs = qs.filter(place__in=calendar_permanent_url.places.all())

        if calendar_permanent_url.reasons.exists():
            qs = qs.filter(reason__in=calendar_permanent_url.reasons.all())

        ical_out = calendar_from_queryset(qs)

        response = HttpResponse(ical_out, content_type="content-type:text/calendar")
        response["Content-Disposition"] = "attachment; filename=calendar.ics"

        return response
