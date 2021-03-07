# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import DefaultParamsView, DiagnosticView, ComputeResultsView, ReportPdfView

app_name = "autodiag_copro"

urlpatterns = [
    url(r"^diagnostics$", DiagnosticView.as_view(), name="diagnostic_list"),
    url(r"^diagnostic/$", DiagnosticView.as_view(), name="diagnostic"),
    url(
        r"^diagnostic/(?P<pk>[^/.]+)/$",
        DiagnosticView.as_view(),
        name="diagnostic_detail",
    ),
    url(
        r"^default_params/(?P<user_pk>[^/.]+)/$",
        DefaultParamsView.as_view(),
        name="default_params",
    ),
    url(r"^compute_results$", ComputeResultsView.as_view(), name="compute_results"),
    url(r"^report/pdf$", ReportPdfView.as_view(), name="get_pdf_report"),
]
