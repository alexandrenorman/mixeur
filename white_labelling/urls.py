# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import WhiteLabellingView

app_name = "white_labelling"

urlpatterns = [url(r"^(?P<domain>.*)/$", WhiteLabellingView.as_view(), name="profile")]
