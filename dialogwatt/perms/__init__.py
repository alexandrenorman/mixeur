# -*- coding: utf-8 -*-

from .appointment_perm import AppointmentPermissionLogic
from .calendar_permanent_url_perm import CalendarPermanentUrlPermissionLogic
from .catchment_area_perm import CatchmentAreaPermissionLogic
from .exchange_perm import ExchangePermissionLogic
from .exchange_attachment_perm import ExchangeAttachmentPermissionLogic
from .notification_perm import NotificationPermissionLogic
from .notification_requested_perm import NotificationRequestedPermissionLogic
from .place_perm import PlacePermissionLogic
from .reason_perm import ReasonPermissionLogic
from .slot_perm import SlotPermissionLogic
from .slot_informations_perm import SlotInformationsPermissionLogic

__all__ = [
    "AppointmentPermissionLogic",
    "CalendarPermanentUrlPermissionLogic",
    "CatchmentAreaPermissionLogic",
    "ExchangePermissionLogic",
    "ExchangeAttachmentPermissionLogic",
    "NotificationPermissionLogic",
    "NotificationRequestedPermissionLogic",
    "PlacePermissionLogic",
    "ReasonPermissionLogic",
    "SlotInformationsPermissionLogic",
    "SlotPermissionLogic",
]
