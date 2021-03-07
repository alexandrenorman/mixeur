# -*- coding: utf-8 -*-
import json
from pdf_generator.utils import build_pdf_stream_from
from django.http import JsonResponse

from helpers.views import ApiView

from pdf_generator.forms import PdfTempStoreForm
from pdf_generator.serializers import PdfTempStoreSerializer

from autodiag_copro.models import Params, DefaultParams, CombustibleParams
from autodiag_copro.serializers import (
    ParamsSerializer,
    AbstractCombustibleParamsWithYearlySerializer,
)


def get_and_format_params(request, data):
    heating_combustible = data["general_infos"]["heating_combustible"]

    if data["diagnostic"]["pk"] is not None:
        # Get diagnostic params
        main_params = Params.objects.get(diagnostic=data["diagnostic"]["pk"])
        combustible_params = CombustibleParams.objects.get(
            params_id=main_params.id, combustible=heating_combustible
        )
    elif (
        request.user is not None
        and not request.user.is_anonymous
        and request.user.is_advisor
    ):
        main_params = data["params"]["main_params"]
        combustible_params = [
            x
            for x in data["params"]["combustibles_params"]
            if x["combustible"] == heating_combustible
        ]
    else:
        # Get group params
        main_params = DefaultParams.default_value(
            key=None
        )  # FIXME: Replace None by group_id with white_labelling
        combustible_params = main_params.combustible_params.get(
            combustible=heating_combustible
        )

    if type(main_params) != dict:
        main_params = ParamsSerializer(main_params).data
        combustible_params = AbstractCombustibleParamsWithYearlySerializer(
            combustible_params
        ).data

    return {"main_params": main_params, "combustibles_params": combustible_params}


class ReportPdfView(ApiView):
    """
    PdfView
    """

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        domain = data["domain"]
        data = data["data"]

        print("-- Build Diagnostic Results PDF --")
        print()

        data["params"] = get_and_format_params(request, data)

        # persist params in PdfTemp
        store = PdfTempStoreForm({"data": data})
        if store.is_valid():
            store_instance = store.save()
        else:
            return JsonResponse({"error": "Pdf data is invalid"})

        uuid = PdfTempStoreSerializer(store_instance).data["uuid"]
        url = f"http://nginx/#/autodiag-copro/rapport-de-diagnostic/{uuid}/pdf?domain={domain}"
        print(url)

        pdf = build_pdf_stream_from(url)
        store_instance.delete()

        return pdf
