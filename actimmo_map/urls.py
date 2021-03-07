# -*- coding: utf-8 -*-
from django.conf.urls import url

from actimmo_map.views import (
    ActimmoContactView,
    ActimmoIconsView,
    ActimmoMapView,
    ActimmoPartnersView,
)

app_name = "actimmo_map"

urlpatterns = [
    url(r"^actimmo-map/$", ActimmoMapView.as_view(), name="actimmo_map_view"),
    url(
        r"^actimmo-contact/$", ActimmoContactView.as_view(), name="actimmo_contact_view"
    ),
    url(
        r"^actimmo-partners/$",
        ActimmoPartnersView.as_view(),
        name="actimmo_partners_view",
    ),
    url(
        r"^actimmo-icons/$",
        ActimmoIconsView.as_view(),
        name="actimmo_icons_view",
    ),
]
