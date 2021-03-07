# -*- coding: utf-8 -*-
from django.conf.urls import url

from visit_report.views import (
    AdvisorForHousingView,
    EntitiesListView,
    FaceView,
    FinancialAidView,
    FinancingView,
    HousingView,
    ScenarioView,
    ScenarioSummaryView,
    StepView,
    SystemView,
    ReportView,
    WorkRecommendationView,
    ReportPdfView,
)

app_name = "visit_report"

urlpatterns = [
    url(r"^report/pdf$", ReportPdfView.as_view(), name="get_pdf_report"),
    url(r"^face/$", FaceView.as_view(), name="face_list"),
    url(r"^face/(?P<pk>[^/.]+)/$", FaceView.as_view(), name="face_detail"),
    url(r"^financial-aid/$", FinancialAidView.as_view(), name="financial_aid_list"),
    url(
        r"^financial-aid/(?P<pk>[^/.]+)/$",
        FinancialAidView.as_view(),
        name="financial_aid_detail",
    ),
    url(r"^financing/$", FinancingView.as_view(), name="financing_list"),
    url(
        r"^financing/(?P<pk>[^/.]+)/$", FinancingView.as_view(), name="financing_detail"
    ),
    url(r"^housing/$", HousingView.as_view(), name="housing_list"),
    url(r"^housing/(?P<pk>[^/.]+)/$", HousingView.as_view(), name="housing_detail"),
    url(r"^scenario/$", ScenarioView.as_view(), name="scenario_list"),
    url(r"^scenario/(?P<pk>[^/.]+)/$", ScenarioView.as_view(), name="scenario_detail"),
    url(
        r"^scenario-summary/$",
        ScenarioSummaryView.as_view(),
        name="scenario_summary_list",
    ),
    url(
        r"^scenario-summary/(?P<pk>[^/.]+)/$",
        ScenarioSummaryView.as_view(),
        name="scenario_summary_detail",
    ),
    url(r"^step/$", StepView.as_view(), name="step_list"),
    url(r"^step/(?P<pk>[^/.]+)/$", StepView.as_view(), name="step_detail"),
    url(r"^system/$", SystemView.as_view(), name="system_list"),
    url(r"^system/(?P<pk>[^/.]+)/$", SystemView.as_view(), name="system_detail"),
    url(r"^report/$", ReportView.as_view(), name="visit_report_list"),
    url(r"^report/(?P<pk>[^/.]+)/$", ReportView.as_view(), name="visit_report_detail"),
    url(
        r"^work-recommendation/$",
        WorkRecommendationView.as_view(),
        name="work_recommendation_list",
    ),
    url(
        r"^work-recommendation/(?P<pk>[^/.]+)/$",
        WorkRecommendationView.as_view(),
        name="work_recommendation_detail",
    ),
    url(
        r"^advisors-for-housing/(?P<pk>[^/.]+)/$",
        AdvisorForHousingView.as_view(),
        name="advisor_for_housing",
    ),
    url(
        r"^entities/$",
        EntitiesListView.as_view(),
        name="entities_list",
    ),
]
