# -*- coding: utf-8 -*-
from django.conf.urls import url

from custom_forms.views import (
    CustomFormLastUpdateView,
    CustomFormView,
)

app_name = "custom_forms"

urlpatterns = [
    url(
        r"^custom-form/(?P<model>[\w\-]+)/(?P<anchor>[\w\-]+)/$",
        CustomFormView.as_view(),
        name="custom_form_view",
    ),
    url(
        r"^custom-form/last-update/$",
        CustomFormLastUpdateView.as_view(),
        name="custom_form_last_update_view",
    ),
]
