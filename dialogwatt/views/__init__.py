# -*- coding: utf-8 -*-

from .appointment_booking_for_advisor_view import AppointmentBookingForAdvisorView
from .appointment_booking_view import AppointmentBookingView
from .appointment_tmp_booking_view import AppointmentTmpBookingView
from .appointment_view import AppointmentView
from .calendar_for_slots_view import CalendarForSlotsView
from .calendar_permanent_url_for_slots_view import CalendarPermanentUrlForSlotsView
from .calendar_permanent_url_public_for_slots_view import (
    CalendarPermanentUrlPublicForSlotsView,
)
from .calendar_permanent_url_public_view import CalendarPermanentUrlPublicView
from .calendar_permanent_url_view import CalendarPermanentUrlView
from .calendar_view import CalendarView
from .catchment_area_view import CatchmentAreaView
from .create_client_and_contact_with_rgpd_view import CreateClientAndContactWithRgpdView
from .exchange_view import ExchangeView
from .find_advisors_for_reason_view import FindAdvisorsForReasonView
from .find_appointment_view import FindAppointmentView
from .find_catchment_areas_from_inseecode_view import (
    FindCatchmentAreasFromInseecodeView,
)
from .find_place_from_slug_view import FindPlaceFromSlugView
from .find_places_from_inseecode_view import FindPlacesFromInseecodeView
from .find_reasons_from_inseecode_view import FindReasonsFromInseecodeView
from .notification_view import NotificationView
from .place_view import PlaceView
from .reason_view import ReasonView
from .slot_duplicate_to_dates_view import SlotDuplicateToDatesView
from .slot_has_appointments_view import SlotHasAppointmentsView
from .slot_informations_view import SlotInformationsView
from .slot_view import SlotView
from .validate_appointment_booking_view import ValidateAppointmentBookingView


__all__ = [
    "AppointmentBookingForAdvisorView",
    "AppointmentBookingView",
    "AppointmentTmpBookingView",
    "AppointmentView",
    "CalendarForSlotsView",
    "CalendarPermanentUrlForSlotsView",
    "CalendarPermanentUrlPublicForSlotsView",
    "CalendarPermanentUrlPublicView",
    "CalendarPermanentUrlView",
    "CalendarView",
    "CatchmentAreaView",
    "CreateClientAndContactWithRgpdView",
    "ExchangeView",
    "FindAdvisorsForReasonView",
    "FindAppointmentView",
    "FindCatchmentAreasFromInseecodeView",
    "FindPlaceFromSlugView",
    "FindPlacesFromInseecodeView",
    "FindReasonsFromInseecodeView",
    "NotificationView",
    "PlaceView",
    "ReasonView",
    "SlotDuplicateToDatesView",
    "SlotHasAppointmentsView",
    "SlotInformationsView",
    "SlotView",
    "ValidateAppointmentBookingView",
]
