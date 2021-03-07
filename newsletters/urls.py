# -*- coding: utf-8 -*-
from django.conf.urls import url

from newsletters.views import (
    GroupOfNewslettersView,
    GroupOfNewslettersPublicView,
    ImageView,
    NewsletterView,
    NewsletterPublicView,
    PremailerView,
)

app_name = "newsletters"

urlpatterns = [
    url(
        r"^group-of-newsletters/$",
        GroupOfNewslettersView.as_view(),
        name="group_of_newsletters_list",
    ),
    url(
        r"^group-of-newsletters/(?P<pk>[^/.]+)/$",
        GroupOfNewslettersView.as_view(),
        name="group_of_newsletters_detail",
    ),
    url(r"^image/$", ImageView.as_view(), name="image_list"),
    url(r"^image/(?P<pk>[^/.]+)/$", ImageView.as_view(), name="image_detail"),
    url(r"^newsletter/$", NewsletterView.as_view(), name="newsletter_list"),
    url(
        r"^newsletter/(?P<pk>[^/.]+)/$",
        NewsletterView.as_view(),
        name="newsletter_detail",
    ),
    url(r"^premailer/$", PremailerView.as_view(), name="premailer"),
    # public views
    url(
        r"^group-of-newsletters-public/$",
        GroupOfNewslettersPublicView.as_view(),
        name="group_of_newsletters_public_list",
    ),
    url(
        r"^group-of-newsletters-public/(?P<pk>[^/.]+)/$",
        GroupOfNewslettersPublicView.as_view(),
        name="group_of_newsletters_public_detail",
    ),
    url(
        r"^newsletter-public/$",
        NewsletterPublicView.as_view(),
        name="newsletter_public_list",
    ),
    url(
        r"^newsletter-public/(?P<pk>[^/.]+)/$",
        NewsletterPublicView.as_view(),
        name="newsletter_public_detail",
    ),
]
