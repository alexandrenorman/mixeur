# -*- coding: utf-8 -*-
from django.conf.urls import url

from dialogwatt.views import (
    AppointmentBookingForAdvisorView,
    AppointmentBookingView,
    AppointmentTmpBookingView,
    AppointmentView,
    CalendarForSlotsView,
    CalendarPermanentUrlForSlotsView,
    CalendarPermanentUrlPublicForSlotsView,
    CalendarPermanentUrlPublicView,
    CalendarPermanentUrlView,
    CalendarView,
    CatchmentAreaView,
    CreateClientAndContactWithRgpdView,
    ExchangeView,
    FindAdvisorsForReasonView,
    FindAppointmentView,
    FindCatchmentAreasFromInseecodeView,
    FindPlaceFromSlugView,
    FindPlacesFromInseecodeView,
    FindReasonsFromInseecodeView,
    NotificationView,
    PlaceView,
    ReasonView,
    SlotDuplicateToDatesView,
    SlotHasAppointmentsView,
    SlotInformationsView,
    SlotView,
    # ValidateAppointmentBookingView,
)

app_name = "dialogwatt"

urlpatterns = [
    # Appointments ical
    url(r"^ical/$", CalendarView.as_view(), name="calendar_view"),
    url(
        r"^ical-permanent-url/$",
        CalendarPermanentUrlView.as_view(),
        name="calendar_permanent_url_view",
    ),
    url(
        r"^ical-permanent-url/(?P<unique_id>[0-9a-z-]+)/$",
        CalendarPermanentUrlPublicView.as_view(),
        name="calendar_permanent_url_public_view",
    ),
    # Slots ical
    url(
        r"^ical-for-slots/$",
        CalendarForSlotsView.as_view(),
        name="calendar_for_slots_view",
    ),
    url(
        r"^ical-permanent-url-for-slots/$",
        CalendarPermanentUrlForSlotsView.as_view(),
        name="calendar_permanent_url_for_slots_view",
    ),
    url(
        r"^ical-permanent-url-for-slots/(?P<unique_id>[0-9a-z-]+)/$",
        CalendarPermanentUrlPublicForSlotsView.as_view(),
        name="calendar_permanent_url_public_for_slots_view",
    ),
    url(
        r"^book-appointment/$",
        AppointmentBookingView.as_view(),
        name="appointment_book",
    ),
    url(
        r"^book-appointment-tmp/$",
        AppointmentTmpBookingView.as_view(),
        name="appointment_book_tmp",
    ),
    url(
        r"^book-appointment-tmp/(?P<pk>[^/.]+)/(?P<uuid>[0-9a-z-]+)/$",
        AppointmentTmpBookingView.as_view(),
        name="appointment_book_tmp_update",
    ),
    url(r"^appointment/$", AppointmentView.as_view(), name="appointment_list"),
    url(
        r"^appointment/(?P<pk>[^/.]+)/$",
        AppointmentView.as_view(),
        name="appointment_detail",
    ),
    # TBD: remove later
    url(
        r"^catchment_area/$",
        CatchmentAreaView.as_view(),
        name="catchment_area_list_old",
    ),
    url(
        r"^catchment_area/(?P<pk>[^/.]+)/$",
        CatchmentAreaView.as_view(),
        name="catchment_area_detail_old",
    ),
    # /TBD: remove later
    url(r"^catchment-area/$", CatchmentAreaView.as_view(), name="catchment_area_list"),
    url(
        r"^catchment-area/(?P<pk>[^/.]+)/$",
        CatchmentAreaView.as_view(),
        name="catchment_area_detail",
    ),
    url(r"^place/$", PlaceView.as_view(), name="place_list"),
    url(r"^place/(?P<pk>[^/.]+)/$", PlaceView.as_view(), name="place_detail"),
    url(
        r"^places-from-inseecode/(?P<inseecode>[^/.]+)/(?P<reason>[^/.]+)/$",
        FindPlacesFromInseecodeView.as_view(),
        name="places_from_inseecode",
    ),
    url(
        r"^place-from-slug/(?P<slug>[^/.]+)/$",
        FindPlaceFromSlugView.as_view(),
        name="place_from_slug",
    ),
    url(r"^slot/$", SlotView.as_view(), name="slot_list"),
    url(r"^slot/(?P<pk>[^/.]+)/$", SlotView.as_view(), name="slot_detail"),
    url(
        r"^slot-duplicate-to-dates/$",
        SlotDuplicateToDatesView.as_view(),
        name="slot_duplicate_to_dates",
    ),
    url(
        r"^slot-has-appointments/(?P<pk>[^/.]+)/$",
        SlotHasAppointmentsView.as_view(),
        name="slot_has_appointments",
    ),
    url(
        r"^slot-informations/(?P<pk>[^/.]+)/$",
        SlotInformationsView.as_view(),
        name="slot_informations",
    ),
    url(r"^reason/$", ReasonView.as_view(), name="reason_list"),
    url(r"^reason/(?P<pk>[^/.]+)/$", ReasonView.as_view(), name="reason_detail"),
    url(r"^notification/$", NotificationView.as_view(), name="notification_list"),
    url(
        r"^notification/(?P<pk>[^/.]+)/$",
        NotificationView.as_view(),
        name="notification_detail",
    ),
    url(r"^exchange/$", ExchangeView.as_view(), name="exchange_list"),
    url(r"^exchange/(?P<pk>[^/.]+)/$", ExchangeView.as_view(), name="exchange_detail"),
    url(r"^find-appointment/$", FindAppointmentView.as_view(), name="find_appointment"),
    url(
        r"^find-reasons-from-inseecode/(?P<inseecode>[0-9]+)/$",
        FindReasonsFromInseecodeView.as_view(),
        name="find_reasons_from_inseecode_view",
    ),
    url(
        r"^find-catchment-areas-from-inseecode/(?P<inseecode>[0-9]+)/$",
        FindCatchmentAreasFromInseecodeView.as_view(),
        name="find_catchment_areas_from_inseecode_view",
    ),
    url(
        r"^find-advisors-for-reason/$",
        FindAdvisorsForReasonView.as_view(),
        name="find_advisors_for_reason_view",
    ),
    url(
        r"^appointment-booking-for-advisor/$",
        AppointmentBookingForAdvisorView.as_view(),
        name="appointment_booking_for_advisor",
    ),
    url(
        r"create-client-and-contact-with-rgpd",
        CreateClientAndContactWithRgpdView.as_view(),
        name="create_client_and_contact_with_rgpd_view",
    ),
]
