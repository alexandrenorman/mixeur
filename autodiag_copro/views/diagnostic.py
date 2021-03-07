# -*- coding: utf-8 -*-
from rest_framework import status

from django.http import JsonResponse
from django.db import transaction, IntegrityError
from django.shortcuts import get_object_or_404
import json

from helpers.views import LoginRequiredApiView

from autodiag_copro.libs.compute import build_years

from autodiag_copro.models import (
    Diagnostic,
    Copro,
    YearlyData,
    Params,
    DefaultParams,
    YearlyParams,
    CombustibleParams,
    YearlyCombustibleParams,
)

from autodiag_copro.forms import (
    DiagnosticForm,
    CoproForm,
    YearlyDataForm,
    ParamsForm,
    YearlyParamsForm,
    CombustibleParamsForm,
    YearlyCombustibleParamsForm,
)

from accounts.serializers import UserSimpleSerializer
from autodiag_copro.serializers import (
    SimpleDiagnosticSerializer,
    AbstractGeneralInfosSerializer,
    GeneralInfosSerializer,
    AbstractYearlyDataSerializer,
    YearlyDataSerializer,
    AbstractParamsSerializer,
    ParamsSerializer,
    AbstractCombustibleParamsSerializer,
    CombustibleParamsSerializer,
    AbstractYearlyCombustibleParamsSerializer,
    YearlyCombustibleParamsSerializer,
    AbstractCombustibleParamsWithYearlySerializer,
)


class DiagnosticView(LoginRequiredApiView):
    """
    DiagnosticView requires authenticated user

    get :model:`autodiag_copro.Diagnostic`

    """

    def get(self, request, *args, **kwargs):
        """
        """
        if "pk" in kwargs:
            return self.detail(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)

    def detail(self, request, *args, **kwargs):
        """
        Get :model:`autodiag_copro.Diagnostic` by [pk]
        """
        pk = kwargs["pk"]
        diagnostic = Diagnostic.objects.get(pk=pk)

        if not request.user.has_perm("autodiagCopro.view", diagnostic):
            return JsonResponse(
                {"error": "change not permitted"}, status=status.HTTP_403_FORBIDDEN
            )

        combustibles_params_ids = diagnostic.params.combustible_params.values_list(
            "id", flat=True
        )
        yearly_combustibles_params = YearlyCombustibleParams.objects.filter(
            combustible_params__in=combustibles_params_ids
        )

        if request.GET["last_year"] != "":
            last_year = int(request.GET["last_year"])
            main_params = AbstractParamsSerializer(diagnostic.params).data
            combustible_params = AbstractCombustibleParamsSerializer(
                diagnostic.params.combustible_params.all(), many=True
            ).data
            yearly_combustibles_params = AbstractYearlyCombustibleParamsSerializer(
                yearly_combustibles_params, many=True
            ).data
            general_infos = AbstractGeneralInfosSerializer(diagnostic.copro).data
            yearly_datum = AbstractYearlyDataSerializer(
                diagnostic.copro.yearly_data.all(), many=True
            ).data
            diagnostic.pk = None
        else:
            last_year = diagnostic.last_year
            main_params = ParamsSerializer(diagnostic.params).data
            combustible_params = CombustibleParamsSerializer(
                diagnostic.params.combustible_params.all(), many=True
            ).data
            yearly_combustibles_params = YearlyCombustibleParamsSerializer(
                yearly_combustibles_params, many=True
            ).data
            general_infos = GeneralInfosSerializer(diagnostic.copro).data
            yearly_datum = YearlyDataSerializer(
                diagnostic.copro.yearly_data.all(), many=True
            ).data

        years = build_years(last_year)
        for index, year in enumerate(years):
            if (
                len(
                    [
                        yearly_data
                        for yearly_data in yearly_datum
                        if yearly_data["years"] == year
                    ]
                )
                == 0
            ):
                yearly_datum.insert(
                    index,
                    {
                        "pk": None,
                        "years": year,
                        "heating_energy_charges": None,
                        "energy_consumption": None,
                        "hot_water_energy_charges": None,
                        "hot_water_consumption_charges": None,
                        "hot_water_consumption": None,
                        "water_consumption_charges": None,
                        "water_consumption": None,
                        "dju_correction": None,
                    },
                )

        yearly_datum.sort(key=lambda x: int(x["years"][0:4]), reverse=True)

        return JsonResponse(
            {
                "diagnostic": SimpleDiagnosticSerializer(diagnostic).data,
                "main_params": main_params,
                "combustibles_params": {
                    "combustibles_params": combustible_params,
                    "yearlyCombustibles_params": yearly_combustibles_params,
                },
                "general_infos": general_infos,
                "yearly_data": {"yearly_datum": yearly_datum},
            }
        )

    def list(self, request, *args, **kwargs):
        """
        List :model:`autodiag_copro.Diagnostic`

        Can be filtered by user [?user=pk]
        """
        limit = int(request.GET["limit"])
        page = int(request.GET["page"])
        diagnostics = Diagnostic.objects.all()

        if "user" in request.GET:
            diagnostics = diagnostics.filter(user__pk=request.GET["user"])

        nbDiagnostics = diagnostics.count()
        offset_from = (page - 1) * limit
        offset_to = page * limit
        diagnostics_chunk = diagnostics[offset_from:offset_to]

        serializer = SimpleDiagnosticSerializer(diagnostics_chunk, many=True)
        return JsonResponse(
            {"diagnostics_chunk": serializer.data, "nb_diagnostics": nbDiagnostics},
            safe=False,
        )

    def post(self, request, *args, **kwargs):
        """
        Create :model:`autodiag_copro.Diagnostic` by [pk]

        Must have diagnostic.change permission
        """
        diagnostic_data = json.loads(request.body)
        params = self.get_and_format_params(request, diagnostic_data)

        try:
            with transaction.atomic():
                results = self.create_or_update_diagnostic(
                    request.user, diagnostic_data, params
                )
        except IntegrityError:
            return JsonResponse(
                {"error": "bad request"}, status=status.HTTP_400_BAD_REQUEST
            )

        return JsonResponse(results)

    def patch(self, request, *args, **kwargs):
        """
        Update :model:`autodiag_copro.Diagnostic` by [pk]

        Must have diagnostic.change permission
        """
        try:
            key = kwargs["pk"]
        except KeyError:
            return JsonResponse(
                {"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        diagnostic_data = json.loads(request.body)

        pk = key
        diagnostic = get_object_or_404(Diagnostic, pk=pk)

        if not request.user.has_perm("autodiagCopro.change", diagnostic):
            return JsonResponse(
                {"error": "change not permitted"}, status=status.HTTP_403_FORBIDDEN
            )

        params = self.get_and_format_params(request, diagnostic_data)

        try:
            with transaction.atomic():
                results = self.create_or_update_diagnostic(
                    request.user, diagnostic_data, params
                )
        except IntegrityError:
            return JsonResponse(
                {"error": "bad request"}, status=status.HTTP_400_BAD_REQUEST
            )

        return JsonResponse(results)

    def delete(self, request, *args, **kwargs):
        """
        Delete :model:`autodiag_copro.Diagnostic` by [pk]

        Must have diagnostic.change permission
        """
        try:
            key = kwargs["pk"]
        except KeyError:
            return JsonResponse(
                {"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        pk = key
        diagnostic = get_object_or_404(Diagnostic, pk=pk)

        if not request.user.has_perm("autodiagCopro.delete", diagnostic):
            return JsonResponse(
                {"error": "delete not permitted"}, status=status.HTTP_403_FORBIDDEN
            )

        diagnostic.delete()

        return JsonResponse({"ok": "Deleted"})

    def get_and_format_params(self, request, data):
        if (
            request.user is not None
            and not request.user.is_anonymous
            and request.user.is_advisor
        ):
            # Get custom advisor params
            main_params = data["params"]["main_params"]
            combustibles_params = data["params"]["combustibles_params"]
            for combustible_params in combustibles_params:
                combustible_params["yearly_combustible_params"] = [
                    x
                    for x in data["params"]["yearly_combustibles_params"]
                    if x["pk"] in combustible_params["yearly_combustible_params_ids"]
                ]
        else:
            # Get group params
            main_params = DefaultParams.default_value(
                key=None
            )  # FIXME: Replace None by group_id with white_labelling
            combustibles_params = main_params.combustible_params.all()

            main_params = AbstractParamsSerializer(main_params).data
            combustibles_params = [
                AbstractCombustibleParamsWithYearlySerializer(x).data
                for x in combustibles_params
            ]

        return {"main_params": main_params, "combustibles_params": combustibles_params}

    def create_or_update_diagnostic(self, user, diagnostic_data, params):  # noqa: C901
        # Force duplicate diagnostic if user's diagnostic is, for the first time, edited by an advisor
        force_create = (
            user.is_advisor and diagnostic_data["diagnostic"]["advisor"] is None
        )

        # COPRO
        copro = self.__save_copro(diagnostic_data["general_infos"], force_create)

        # YEARLY_DATA
        yearly_datum = []
        for yearly_data in diagnostic_data["yearly_data"]["yearly_datum"]:
            if (
                yearly_data["heating_energy_charges"] is None
                and yearly_data["energy_consumption"] is None
                and (
                    not copro.with_dju_correction
                    or (
                        copro.with_dju_correction
                        and yearly_data["dju_correction"] is None
                    )
                )
            ):
                yearly_datum.append(self.__delete_yearly_data(yearly_data))
            else:
                yearly_data["copro"] = copro.id
                yearly_datum.append(
                    YearlyDataSerializer(
                        self.__save_yearly_data(yearly_data, force_create)
                    ).data
                )

        # PARAMS
        main_params = self.__save_main_params(params, force_create)

        # YEARLY_PARAMS
        for yearly_params in params["main_params"]["yearly_params"]:
            yearly_params["params"] = main_params.id
            self.__save_yearly_params(yearly_params, force_create)

        # COMBUSTIBLE_PARAMS
        combustibles_params = []
        yearly_combustibles_params = []

        for combustible_params_data in params["combustibles_params"]:
            combustible_params_data["params"] = main_params.id
            combustible_params = self.__save_combustible_params(
                combustible_params_data, force_create
            )
            combustibles_params.append(combustible_params)

            # YEARLY_COMBUSTIBLE_PARAMS
            for yearly_combustible_params_data in combustible_params_data[
                "yearly_combustible_params"
            ]:
                yearly_combustible_params_data[
                    "combustible_params"
                ] = combustible_params.id
                yearly_combustible_params = self.__save_yearly_combustible_params(
                    yearly_combustible_params_data, force_create
                )
                yearly_combustibles_params.append(yearly_combustible_params)

        diagnostic = self.__save_diagnostic(
            diagnostic_data["diagnostic"],
            {
                "last_year": diagnostic_data["diagnostic"]["last_year"],
                "user": diagnostic_data["diagnostic"]["user"]["pk"],
                "advisor": user.pk if user.is_advisor else None,
                "copro": copro.id,
                "params": main_params.id,
                "comments": diagnostic_data["diagnostic"]["comments"],
            },
            force_create,
        )

        general_infos = GeneralInfosSerializer(copro).data

        return {
            "diagnostic": {
                "pk": diagnostic.pk,
                "user": UserSimpleSerializer(diagnostic.user).data,
                "advisor": UserSimpleSerializer(diagnostic.advisor).data
                if diagnostic.advisor is not None
                else None,
                "last_year": diagnostic.last_year,
                "comments": diagnostic.comments,
            },
            "main_params": ParamsSerializer(main_params).data,
            "combustibles_params": {
                "combustibles_params": CombustibleParamsSerializer(
                    combustibles_params, many=True
                ).data,
                "yearly_combustibles_params": YearlyCombustibleParamsSerializer(
                    yearly_combustibles_params, many=True
                ).data,
            },
            "general_infos": general_infos,
            "yearly_data": {"yearly_datum": yearly_datum},
        }

    def __save_copro(self, general_infos, force_create):
        if (
            not force_create
            and "pk" in general_infos.keys()
            and general_infos["pk"] is not None
        ):
            copro_instance = get_object_or_404(Copro, pk=general_infos["pk"])
            copro_form = CoproForm(general_infos, instance=copro_instance)
        else:
            copro_form = CoproForm(general_infos)
        if copro_form.is_valid():
            return copro_form.save()
        else:
            raise IntegrityError()

    def __save_yearly_data(self, yearly_data, force_create):
        if (
            not force_create
            and "pk" in yearly_data.keys()
            and yearly_data["pk"] is not None
        ):
            yearly_data_instance = get_object_or_404(YearlyData, pk=yearly_data["pk"])
            yearly_data_form = YearlyDataForm(
                yearly_data, instance=yearly_data_instance
            )
        else:
            yearly_data_form = YearlyDataForm(yearly_data)
        if yearly_data_form.is_valid():
            yearly_data = yearly_data_form.save()
            return yearly_data
        else:
            raise IntegrityError()

    def __delete_yearly_data(self, yearly_data):
        if "pk" in yearly_data.keys() and yearly_data["pk"] is not None:
            yearly_data_instance = get_object_or_404(YearlyData, pk=yearly_data["pk"])
            yearly_data_instance.delete()
        return {
            "pk": None,
            "years": yearly_data["years"],
            "heating_energy_charges": None,
            "energy_consumption": None,
            "hot_water_energy_charges": None,
            "hot_water_consumption_charges": None,
            "hot_water_consumption": None,
            "water_consumption_charges": None,
            "water_consumption": None,
            "dju_correction": None,
        }

    def __save_main_params(self, params, force_create):
        if (
            not force_create
            and "pk" in params["main_params"].keys()
            and params["main_params"]["pk"] is not None
        ):
            main_params_instance = get_object_or_404(
                Params, pk=params["main_params"]["pk"]
            )
            main_params_form = ParamsForm(
                params["main_params"], instance=main_params_instance
            )
        else:
            main_params_form = ParamsForm(params["main_params"])
        if main_params_form.is_valid():
            return main_params_form.save()
        else:
            raise IntegrityError()

    def __save_yearly_params(self, yearly_params, force_create):
        if (
            not force_create
            and "pk" in yearly_params.keys()
            and yearly_params["pk"] is not None
        ):
            yearly_params_instance = get_object_or_404(
                YearlyParams, pk=yearly_params["pk"]
            )
            yearly_params_form = YearlyParamsForm(
                yearly_params, instance=yearly_params_instance
            )
        else:
            yearly_params_form = YearlyParamsForm(yearly_params)
        if yearly_params_form.is_valid():
            yearly_params_form.save()
            return yearly_params
        else:
            raise IntegrityError()

    def __save_combustible_params(self, combustible_params_data, force_create):
        if (
            not force_create
            and "pk" in combustible_params_data.keys()
            and combustible_params_data["pk"] is not None
        ):
            combustible_params_instance = get_object_or_404(
                CombustibleParams, pk=combustible_params_data["pk"]
            )
            combustible_params_form = CombustibleParamsForm(
                combustible_params_data, instance=combustible_params_instance
            )
        else:
            combustible_params_form = CombustibleParamsForm(combustible_params_data)
        if combustible_params_form.is_valid():
            return combustible_params_form.save()
        else:
            raise IntegrityError()

    def __save_yearly_combustible_params(
        self, yearly_combustible_params_data, force_create
    ):
        if (
            not force_create
            and "pk" in yearly_combustible_params_data.keys()
            and yearly_combustible_params_data["pk"] is not None
        ):
            yearly_combustible_params_instance = get_object_or_404(
                YearlyCombustibleParams, pk=yearly_combustible_params_data["pk"]
            )
            yearly_combustible_params_form = YearlyCombustibleParamsForm(
                yearly_combustible_params_data,
                instance=yearly_combustible_params_instance,
            )
        else:
            yearly_combustible_params_form = YearlyCombustibleParamsForm(
                yearly_combustible_params_data
            )
        if yearly_combustible_params_form.is_valid():
            return yearly_combustible_params_form.save()
        else:
            raise IntegrityError()

    def __save_diagnostic(self, diagnostic_data, diagnostic, force_create):
        if (
            not force_create
            and "pk" in diagnostic_data.keys()
            and diagnostic_data["pk"] is not None
        ):
            diagnostic_instance = get_object_or_404(
                Diagnostic, pk=diagnostic_data["pk"]
            )
            diagnostic_form = DiagnosticForm(diagnostic, instance=diagnostic_instance)
        else:
            diagnostic_form = DiagnosticForm(diagnostic)
        if diagnostic_form.is_valid():
            return diagnostic_form.save()
        else:
            raise IntegrityError()
