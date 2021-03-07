# -*- coding: utf-8 -*-
from django.conf.urls import url

from thermix.views import ComputeResultsView, ReportPdfView

app_name = "thermix"

urlpatterns = [
    url(r"^compute_results$", ComputeResultsView.as_view(), name="compute_results"),
    url(r"^report/pdf$", ReportPdfView.as_view(), name="get_pdf_report"),
]
