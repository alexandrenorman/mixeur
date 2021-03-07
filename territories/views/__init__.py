# -*- coding: utf-8 -*-

from .commune_view import CommuneView
from .departement_view import DepartementView
from .epci_view import EpciView
from .region_view import RegionView
from .other_views import (
    OtherRegionView,
    OtherDepartementView,
    OtherEpciView,
    OtherCommuneView,
    OtherEpciForGroupView,
)
from .quick_region_view import QuickRegionView

__all__ = [
    "CommuneView",
    "DepartementView",
    "EpciView",
    "RegionView",
    "OtherRegionView",
    "OtherDepartementView",
    "OtherEpciView",
    "OtherCommuneView",
    "OtherEpciForGroupView",
    "QuickRegionView",
]
