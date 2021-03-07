# -*- coding: utf-8 -*-
from rest_framework import status
from django.http import JsonResponse
from django.conf import settings

from helpers.views import ModelView, ApiView

from pdf_generator.models import PdfTempStore
from pdf_generator.forms import PdfTempStoreForm
from pdf_generator.serializers import PdfTempStoreSerializer


class PdfTempStoreView(ModelView, ApiView):
    model = PdfTempStore
    form = PdfTempStoreForm
    serializer = PdfTempStoreSerializer

    def detail(self, request, *args, **kwargs):
        if settings.DEBUG or request.META["HTTP_USER_AGENT"] == "PdfGenerator":
            return super().detail(request, *args, **kwargs)

        return JsonResponse(
            {"error": "view not permitted"}, status=status.HTTP_403_FORBIDDEN
        )
