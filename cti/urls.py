# -*- coding: utf-8 -*-
from django.urls import path


from cti.views import (
    CtiView,
)

app_name = "cti"

urlpatterns = [
    # url(r"^/(?P<phone>[^\+?1?\d{9,15}]+)/$", CtiView.as_view(), name="cti_search"),  # NOQA: FS003
    path("<str:phone>/", CtiView.as_view(), name="cti_search"),
]
