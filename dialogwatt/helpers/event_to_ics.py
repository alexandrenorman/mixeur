# -*- coding: utf-8 -*-
from datetime import datetime

from bs4 import BeautifulSoup

import icalendar

from dialogwatt.models import Appointment, Slot


def event_to_ics(event):  # NOQA: C901
    ics_entry = icalendar.Event()
    if event.subject is not None:
        if type(event) == Slot:
            subject = f"Créneau - {event.subject}"
        elif type(event) == Appointment:
            subject = (
                f"Rdv de {event.client_or_contact.full_name} - {event.subject}"
                if event.client_or_contact
                else f"{event.subject}"
            )
        else:
            subject = f"{event.subject}"

    if type(event) == Appointment and event.status == "waiting":
        ics_entry.add("summary", "[en attente]" + subject)
    else:
        ics_entry.add("summary", subject)

    ics_entry.add("dtstart", event.start_date)
    ics_entry.add("dtend", event.end_date)
    ics_entry.add("last-modified", event.updated_at)
    if event.sequence > 0:
        ics_entry.add("sequence", event.sequence)

    ics_entry.add("dtstamp", datetime.now())
    uid = str(event.uuid)
    ics_entry.add("uid", f"{uid}")

    if event.status == "cancelled":
        ics_entry.add("status", "CANCELLED")

    if event.place:
        ics_entry["location"] = icalendar.vText(event.place.name)

    if type(event) == Slot:
        for advisor in event.advisors.all():
            attendee = icalendar.vCalAddress(advisor.email)
            attendee.params["cn"] = icalendar.vText(advisor.full_name)
            attendee.params["ROLE"] = icalendar.vText("REQ-PARTICIPANT")
            ics_entry.add("attendee", attendee, encode=0)

    if type(event) == Appointment:
        if event.advisor:
            attendee = icalendar.vCalAddress(event.advisor.email)
            attendee.params["cn"] = icalendar.vText(event.advisor.full_name)
            attendee.params["ROLE"] = icalendar.vText("REQ-PARTICIPANT")
            ics_entry.add("attendee", attendee, encode=0)

        if event.client_or_contact:
            attendee = icalendar.vCalAddress(f"MAILTO:{event.client_or_contact.email}")
            attendee.params["cn"] = icalendar.vText(event.client_or_contact.full_name)
            attendee.params["ROLE"] = icalendar.vText("REQ-PARTICIPANT")
            ics_entry.add("attendee", attendee, encode=0)

    soup = BeautifulSoup(event.description, features="html5lib")
    description = soup.get_text().replace("\n", "\n\n")
    description += "\n"
    if type(event) == Slot:
        for advisor in event.advisors.all():
            description += "\n - " + advisor.full_name
        if event.place:
            description += "\n@ " + event.place.name
        for reason in event.reasons.all():
            description += "\n - " + reason.name
    if type(event) == Appointment:
        if event.advisor:
            description += "\n - Conseiller " + event.advisor.full_name

        if event.client_or_contact:
            description += "\n - " + event.client_or_contact.full_name
            description += "\n - " + event.client_or_contact.email
            description += (
                ("\n - " + event.client_or_contact.address)
                if event.client_or_contact._meta.label == "fac.Contact"
                else ""
            )
            description += (
                f"\n - {event.client_or_contact.phone}"
                if event.client_or_contact.phone is not None
                else ""
            )
            description += (
                f"\n - {event.client_or_contact.mobile_phone}"
                if event.client_or_contact.mobile_phone is not None
                else ""
            )
        if event.place:
            description += "\n@ Lieu : " + event.place.name

    ics_entry.add("description", description)
    return ics_entry
