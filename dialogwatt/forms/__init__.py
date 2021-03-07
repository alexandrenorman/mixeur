# -*- coding: utf-8 -*-

from .appointment_booking_form import (
    AppointmentBookingForAdvisorForm,
    AppointmentBookingForm,
)
from .appointment_tmp_booking_form import AppointmentTmpBookingForm
from .appointment_form import AppointmentForm
from .calendar_permanent_url_form import CalendarPermanentUrlForm
from .catchment_area_form import CatchmentAreaForm
from .find_appointment_form import FindAppointmentForm
from .find_places_from_inseecode_form import FindPlacesFromInseecodeForm
from .notification_form import NotificationForm
from .place_form import PlaceForm
from .reason_form import ReasonForm
from .slot_duplicate_to_dates_form import SlotDuplicateToDatesForm
from .slot_form import SlotForm


__all__ = [
    "AppointmentForm",
    "AppointmentBookingForm",
    "AppointmentBookingForAdvisorForm",
    "AppointmentTmpBookingForm",
    "CalendarPermanentUrlForm",
    "CatchmentAreaForm",
    "FindAppointmentForm",
    "FindPlacesFromInseecodeForm",
    "NotificationForm",
    "PlaceForm",
    "ReasonForm",
    "SlotDuplicateToDatesForm",
    "SlotForm",
]
