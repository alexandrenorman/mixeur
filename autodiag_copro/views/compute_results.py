# -*- coding: utf-8 -*-
import json
import datetime
from decimal import Decimal

from django.http import JsonResponse

from helpers.views import ApiView
from helpers.forms import FormProxy

from autodiag_copro.libs import Compute
from energies.libs import get_yearly_energies_prices

from autodiag_copro.models import Params, DefaultParams, CombustibleParams

from autodiag_copro.forms import (
    ParamsForm,
    YearlyParamsForm,
    CombustibleParamsForm,
    YearlyCombustibleParamsForm,
)


def __format_yearly_params(yearly_params):
    formatted_yearly_params = []
    for params in yearly_params:
        yearly_params_form = YearlyParamsForm(params)
        yearly_params_form.is_valid()
        formatted_yearly_params.append(FormProxy(yearly_params_form))
    return formatted_yearly_params


def __format_yearly_combustible_params(yearly_combustible_params):
    formatted_yearly_combustible_params = []
    for params in yearly_combustible_params:
        yearly_combustible_params_form = YearlyCombustibleParamsForm(params)
        yearly_combustible_params_form.is_valid()
        formatted_yearly_combustible_params.append(
            FormProxy(yearly_combustible_params_form)
        )
    return formatted_yearly_combustible_params


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
        # Get custom advisor params
        main_params_form = ParamsForm(data["params"]["main_params"])
        main_params_form.is_valid()
        main_params = FormProxy(main_params_form)
        yearly_main_params = __format_yearly_params(
            data["params"]["main_params"]["yearly_params"]
        )
        combustible_params = [
            x
            for x in data["params"]["combustibles_params"]
            if x["combustible"] == heating_combustible
        ][0]
        yearly_combustible_params = __format_yearly_combustible_params(
            data["params"]["yearly_combustibles_params"]
        )
        combustible_params_form = CombustibleParamsForm(combustible_params)
        combustible_params_form.is_valid()
        combustible_params = FormProxy(combustible_params_form)
    else:
        # Get group params
        main_params = DefaultParams.default_value(
            key=None
        )  # FIXME: Replace None by group_id with white_labelling
        combustible_params = main_params.combustible_params.get(
            combustible=heating_combustible
        )

    if type(main_params) != FormProxy:
        yearly_main_params = main_params.yearly_params.all()
        yearly_combustible_params = combustible_params.yearly_combustible_params.all()

    return {
        "main_params": main_params,
        "yearly_main_params": yearly_main_params,
        "combustible_params": combustible_params,
        "yearly_combustible_params": yearly_combustible_params,
    }


class ComputeResultsView(ApiView):
    """
    ComputeResultsView
    """

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body, parse_float=Decimal)

        print("-- Compute Diagnostic Results --")
        print()

        params = get_and_format_params(request, data)

        compute = Compute(data, params)

        now = datetime.datetime.now()
        years = [now.year - 21, now.year - 1]
        energies = [
            "oil",
            "gaz_b1",
            "propane",
            "electricity",
            "wood",
            "shredded_wood",
            "bulk_granules",
            "bag_granules",
        ]
        yearly_energies_prices = get_yearly_energies_prices(energies, years, True)

        return JsonResponse(
            {
                "avg_energy": compute.avg_energy,
                "ref_avg_energy": compute.ref_avg_energy,
                "years": compute.years,
                "yearly_results": compute.yearly_results,
                "yearly_energies_prices": yearly_energies_prices,
            }
        )
