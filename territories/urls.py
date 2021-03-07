# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import CommuneView
from .views import (
    OtherRegionView,
    OtherDepartementView,
    OtherEpciView,
    OtherCommuneView,
    OtherEpciForGroupView,
    QuickRegionView,
)

app_name = "territories"

urlpatterns = [
    url(r"^regions/$", OtherRegionView.as_view(), name="region_list"),
    url(r"^territories/$", QuickRegionView.as_view(), name="territories_list"),
    url(r"^departements/$", OtherDepartementView.as_view(), name="departement_list"),
    url(
        r"^departements/(?P<region_id>[^/.]+)/$",
        OtherDepartementView.as_view(),
        name="departement_list_by_region",
    ),
    url(
        r"^epcis/(?P<departement_id>[^/.]+)/$",
        OtherEpciView.as_view(),
        name="epci_list",
    ),
    url(
        r"^epcis_for_group/$",
        OtherEpciForGroupView.as_view(),
        name="epci_list_for_group",
    ),
    url(r"^commune/$", CommuneView.as_view(), name="commune_list"),
    url(
        r"^communes_by_dep/(?P<departement_id>[^/.]+)/$",
        OtherCommuneView.as_view(),
        name="commune_list_by_departement",
    ),
    url(
        r"^communes_by_epci/(?P<epci_id>[^/.]+)/$",
        OtherCommuneView.as_view(),
        name="commune_list_by_epci",
    ),
    url(
        r"^communes_for_group/(?P<group_id>[^/.]+)/$",
        OtherCommuneView.as_view(),
        name="commune_list_for_group",
    ),
]
