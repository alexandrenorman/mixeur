# -*- coding: utf-8 -*-
import icalendar

from .event_to_ics import event_to_ics


def calendar_from_queryset(qs):
    """
    Return a calendar .ICS file from a given Appointements queryset
    """
    cal = icalendar.Calendar()
    cal.add("prodid", "-//DialogWatt Export ICAL//mxm.dk//")
    cal.add("version", "2.0")
    # cal.add("method", "PUBLISH")

    for event in qs:
        cal.add_component(event_to_ics(event))

    return cal.to_ical()
