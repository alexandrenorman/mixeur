# -*- coding: utf-8 -*-
from django.conf.urls import url

from experiences.views import (
    AssignmentTagView,
    ExperienceView,
    ExperienceTagView,
    ExperienceSponsorView,
    ExplanationView,
    JobTagView,
    PartnerTagView,
    PublicTagView,
    SponsorTagView,
    YearTagView,
)

app_name = "experiences"

urlpatterns = [
    url(r"^assignment-tag/$", AssignmentTagView.as_view(), name="assignment_tag_list"),
    url(
        r"^assignment-tag/(?P<pk>[^/.]+)/$",
        AssignmentTagView.as_view(),
        name="assignment_tag_detail",
    ),
    url(r"^experience/$", ExperienceView.as_view(), name="experience_list"),
    url(
        r"^experience/(?P<pk>[^/.]+)/$",
        ExperienceView.as_view(),
        name="experience_detail",
    ),
    url(r"^experience-tag/$", ExperienceTagView.as_view(), name="experience_tag_list"),
    url(
        r"^experience-tag/(?P<pk>[^/.]+)/$",
        ExperienceTagView.as_view(),
        name="experience_tag_detail",
    ),
    url(
        r"^experience-sponsor/$",
        ExperienceSponsorView.as_view(),
        name="experience_sponsor_list",
    ),
    url(
        r"^experience-sponsor/(?P<pk>[^/.]+)/$",
        ExperienceSponsorView.as_view(),
        name="experience_sponsor_detail",
    ),
    url(r"^explanation/$", ExplanationView.as_view(), name="explanation_list"),
    url(
        r"^explanation/(?P<pk>[^/.]+)/$",
        ExplanationView.as_view(),
        name="explanation_detail",
    ),
    url(r"^job-tag/$", JobTagView.as_view(), name="job_tag_list"),
    url(r"^job-tag/(?P<pk>[^/.]+)/$", JobTagView.as_view(), name="job_tag_detail"),
    url(r"^partner-tag/$", PartnerTagView.as_view(), name="partner_tag_list"),
    url(
        r"^partner-tag/(?P<pk>[^/.]+)/$",
        PartnerTagView.as_view(),
        name="partner_tag_detail",
    ),
    url(r"^public-tag/$", PublicTagView.as_view(), name="public_tag_list"),
    url(
        r"^public-tag/(?P<pk>[^/.]+)/$",
        PublicTagView.as_view(),
        name="public_tag_detail",
    ),
    url(r"^sponsor-tag/$", SponsorTagView.as_view(), name="sponsor_tag_list"),
    url(
        r"^sponsor-tag/(?P<pk>[^/.]+)/$",
        SponsorTagView.as_view(),
        name="sponsor_tag_detail",
    ),
    url(r"^year-tag/$", YearTagView.as_view(), name="year_tag_list"),
    url(r"^year-tag/(?P<pk>[^/.]+)/$", YearTagView.as_view(), name="year_tag_detail"),
]
