import json
from django.conf import settings

from django.http import JsonResponse
from helpers.views import ApiView
from pdf_generator.forms import PdfTempStoreForm
from pdf_generator.serializers import PdfTempStoreSerializer
from pdf_generator.utils import build_pdf_stream_from


class ReportPdfView(ApiView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        # Le domain est nécessaire pour apporter la marque blanche dans l'édition du rapport
        domain = data["domain"]
        data = data["data"]

        print("-- Buid Thermix Report PDF --")
        print()

        # persist params in PdfTemp
        store = PdfTempStoreForm({"data": data})
        if store.is_valid():
            store_instance = store.save()
        else:
            return JsonResponse({"error": "Pdf data is invalid"})

        uuid = PdfTempStoreSerializer(store_instance).data["uuid"]
        url = f"http://nginx/#/thermix/rapport/{uuid}/pdf?domain={domain}"

        if settings.DEBUG:
            print(
                "================================================================================"
            )
            print(url.replace("nginx", domain))
            print(
                "================================================================================"
            )

        pdf = build_pdf_stream_from(url)

        # Clean up database temp store
        if not settings.DEBUG:
            store_instance.delete()

        return pdf
