# -*- coding: utf-8 -*-

from .appointment_admin import AppointmentAdmin
from .calendar_permanent_url_admin import CalendarPermanentUrlAdmin
from .catchment_area_admin import CatchmentAreaAdmin
from .exchange_admin import ExchangeAdmin
from .exchange_attachment_admin import ExchangeAttachmentAdmin
from .place_admin import PlaceAdmin
from .reason_admin import ReasonAdmin
from .slot_admin import SlotAdmin
from .notification_admin import NotificationAdmin
from .notification_requested_admin import NotificationRequestedAdmin


__all__ = [
    "AppointmentAdmin",
    "CalendarPermanentUrlAdmin",
    "CatchmentAreaAdmin",
    "ExchangeAdmin",
    "ExchangeAttachmentAdmin",
    "PlaceAdmin",
    "ReasonAdmin",
    "SlotAdmin",
    "NotificationAdmin",
    "NotificationRequestedAdmin",
]
