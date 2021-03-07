# -*- coding: utf-8 -*-
import json
from django.conf import settings
from pdf_generator.utils import build_pdf_stream_from
from django.http import JsonResponse

from helpers.views import ApiView

from pdf_generator.forms import PdfTempStoreForm
from pdf_generator.serializers import PdfTempStoreSerializer


class ReportPdfView(ApiView):
    """
    PdfView
    """

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        domain = data["domain"]
        data = data["data"]

        print("-- Build Report PDF Export --")
        print()

        # persist params in PdfTemp
        store = PdfTempStoreForm({"data": data})
        if store.is_valid():
            store_instance = store.save()
        else:
            return JsonResponse({"error": "Pdf data is invalid"})

        uuid = PdfTempStoreSerializer(store_instance).data["uuid"]
        url = (
            f"http://nginx/#/compte-rendu-entretien/rapport/{uuid}/pdf?domain={domain}"
        )
        # Early display pdf URL
        if settings.DEBUG:
            print(
                "================================================================================"
            )
            print(url.replace("nginx", domain))
            print(
                "================================================================================"
            )

        pdf = build_pdf_stream_from(url)
        store_instance.delete()

        return pdf
