# -*- coding: utf-8 -*-
from django.conf.urls import url

from ecorenover.views import ReportPdfView

app_name = "ecorenover"

urlpatterns = [url(r"^report/pdf$", ReportPdfView.as_view(), name="get_pdf_report")]
