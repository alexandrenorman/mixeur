# -*- coding: utf-8 -*-

from .commune_serializer import CommuneSerializer
from .commune_for_group_serializer import CommuneForGroupSerializer
from .departement_serializer import DepartementSerializer
from .epci_serializer import EpciSerializer
from .region_serializer import RegionSerializer


__all__ = [
    "CommuneSerializer",
    "CommuneForGroupSerializer",
    "DepartementSerializer",
    "EpciSerializer",
    "RegionSerializer",
]
