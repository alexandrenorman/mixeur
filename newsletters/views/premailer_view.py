# -*- coding: utf-8 -*-
import json

from django.http import JsonResponse

from premailer import transform

from helpers.views import (
    ExpertRequiredApiView,
    ModelView,
    PreventDeleteViewMixin,
    PreventListViewMixin,
    PreventPatchViewMixin,
)


class PremailerView(
    ExpertRequiredApiView,
    PreventListViewMixin,
    PreventDeleteViewMixin,
    PreventPatchViewMixin,
    ModelView,
):
    """
    Premailer View
    """

    model = None
    form = None
    serializer = None
    perm_module = None

    def post(self, request, *args, **kwargs):
        object_data = json.loads(request.body)
        newsletter = object_data["newsletter"]
        fonts = object_data["fonts"]

        premailed = transform(newsletter).replace("<head>", "<head>" + fonts)
        return JsonResponse({"newsletter": premailed})
