# -*- coding: utf-8 -*-

from .place_serializer import PlaceSerializer, PlaceSimpleSerializer
from .place_with_reasons_serializer import PlaceWithReasonsSerializer
from .catchment_area_serializer import (
    CatchmentAreaSerializer,
    CatchmentAreaSimpleSerializer,
)
from .reason_serializer import (
    ReasonSerializer,
    ReasonSimpleSerializer,
    FindReasonsSerializer,
)
from .slot_serializer import (
    SlotSerializer,
    SlotForSchedulerSerializer,
    SlotInformationsSerializer,
)
from .appointment_serializer import (
    AppointmentSerializer,
    AppointmentBookInfoSerializer,
    AppointmentForSchedulerSerializer,
)
from .calendar_permanent_url_serializer import CalendarPermanentUrlSerializer
from .notification_serializer import NotificationSerializer
from .exchange_serializer import ExchangeSerializer


__all__ = [
    "AppointmentForSchedulerSerializer",
    "AppointmentSerializer",
    "AppointmentBookInfoSerializer",
    "CalendarPermanentUrlSerializer",
    "CatchmentAreaSerializer",
    "CatchmentAreaSimpleSerializer",
    "ExchangeSerializer",
    "FindReasonsSerializer",
    "NotificationSerializer",
    "PlaceSerializer",
    "PlaceSimpleSerializer",
    "PlaceWithReasonsSerializer",
    "ReasonSerializer",
    "ReasonSimpleSerializer",
    "SlotForSchedulerSerializer",
    "SlotInformationsSerializer",
    "SlotSerializer",
]
