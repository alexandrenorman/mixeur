# -*- coding: utf-8 -*-
from django.conf.urls import url

from listepro.views.activity_view import ActivityView
from listepro.views.calculation_method_view import CalculationMethodView
from listepro.views.helper_view import HelperView
from listepro.views.job_view import JobView
from listepro.views.key_word_category_view import KeyWordCategoryView
from listepro.views.key_word_view import KeyWordView
from listepro.views.mission_view import MissionView
from listepro.views.pdf_report import PdfReportView
from listepro.views.professional_image_view import ProfessionalImageView
from listepro.views.professional_production_view import ProfessionalProductionView
from listepro.views.professional_view import ProfessionalView
from listepro.views.segment_activity_submission_link_view import (
    SegmentActivitySubMissionLinkView,
)
from listepro.views.segment_view import SegmentView
from listepro.views.sub_mission_view import SubMissionView
from listepro.views.usage_integrated_view import UsageIntegratedView


app_name = "listepro"

urlpatterns = [
    url(
        r"^professional/(?P<pk>[^/.]+)/$",
        ProfessionalView.as_view(),
        name="professional_with_id",
    ),
    url(r"^professional/$", ProfessionalView.as_view(), name="professional"),
    url(r"^segment/$", SegmentView.as_view(), name="segment"),
    url(r"^job/$", JobView.as_view(), name="job"),
    url(r"^mission/$", MissionView.as_view(), name="mission"),
    url(r"^sub-mission/$", SubMissionView.as_view(), name="sub_mission"),
    url(r"^activity/$", ActivityView.as_view(), name="activity"),
    url(r"^key-word/$", KeyWordView.as_view(), name="key_word"),
    url(
        r"^usage-integrated/$",
        UsageIntegratedView.as_view(),
        name="usage_integrated",
    ),
    url(
        r"^calculation-method/$",
        CalculationMethodView.as_view(),
        name="calculation_method",
    ),
    url(
        r"^professional-production/$",
        ProfessionalProductionView.as_view(),
        name="professional_production",
    ),
    url(
        r"^professional-production/(?P<pk>[^/.]+)/$",
        ProfessionalProductionView.as_view(),
        name="professional_production_with_id",
    ),
    url(
        r"^professional-image/$",
        ProfessionalImageView.as_view(),
        name="professional_image",
    ),
    url(
        r"^professional-image/(?P<pk>[^/.]+)/$",
        ProfessionalImageView.as_view(),
        name="professional_image_with_id",
    ),
    url(
        r"^segment-activity-submission-link/$",
        SegmentActivitySubMissionLinkView.as_view(),
        name="segment_activity_submission_link",
    ),
    url(
        r"^key-word-category/$",
        KeyWordCategoryView.as_view(),
        name="key_word_category",
    ),
    url(
        r"^helper/$",
        HelperView.as_view(),
        name="helper",
    ),
    url(r"^helper/(?P<pk>[^/.]+)/$", HelperView.as_view(), name="helper"),
    url(
        r"^pro/(?P<pk>[^/.]+)/$", ProfessionalView.as_view(), name="professional_detail"
    ),
    url(r"^report/pdf$", PdfReportView.as_view(), name="get_report"),
]
