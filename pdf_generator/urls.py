# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import PdfTempStoreView

app_name = "pdf_generator"

urlpatterns = [
    url(
        r"^pdf_temp_store/(?P<pk>[^/.]+)$",
        PdfTempStoreView.as_view(),
        name="pdf_temp_store",
    )
]
