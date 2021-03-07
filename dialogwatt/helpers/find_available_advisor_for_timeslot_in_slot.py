# -*- coding: utf-8 -*-
from dialogwatt.models import Appointment


def find_available_advisor_for_timeslot_in_slot(
    slot, start_date, end_date
) -> Appointment:
    for advisor in slot.advisors.all().order_by("?"):
        if is_advisor_available(advisor, start_date, end_date):
            return advisor

    raise ValueError("Aucun conseiller n'est disponible pour ce créneau")


def is_advisor_available(advisor, start_date, end_date):
    appointments_for_advisor = Appointment.active.filter(
        advisor=advisor, start_date__date=start_date.date()
    )

    for appointment in appointments_for_advisor:
        if (
            start_date < appointment.start_date < end_date
            or start_date < appointment.end_date < end_date
            or (appointment.start_date < start_date and end_date < appointment.end_date)
        ):
            return False

    return True
