# -*- coding: utf-8 -*-
from django.http import JsonResponse

from helpers.views import ApiView

from territories.models import Commune, Departement, Epci, Region


class QuickRegionView(ApiView):
    def get(self, request, *args, **kwargs):
        return self.list_regions(request, *args, **kwargs)

    def get_queryset(self, request, *args, **kwargs):
        qs = Epci.objects.prefetch_related("commune_set").all()
        if (
            "allowed" in request.GET
            and not request.user.is_anonymous
            and request.user.group is not None
            and request.user.group.admin_group is not None
        ):
            qs = qs.filter(
                commune__in=request.user.group.admin_group.territories.all()
            ).distinct()

        return qs

    def list_regions(self, request, *args, **kwargs):  # NOQA: C901, CFQ001
        regions = Region.objects.all().order_by("name").values("pk", "name")
        departements = (
            Departement.objects.order_by("name")
            .all()
            .values("pk", "name", "region__pk")
        )
        communes = (
            Commune.objects.order_by("name")
            .all()
            .values("pk", "name", "epci__pk", "epci__name")
        )
        epcis = (
            Epci.objects.order_by("name")
            .all()
            .values("pk", "name", "commune__departement")
            .distinct()
        )

        if (
            "allowed" in request.GET
            and not request.user.is_anonymous
            and request.user.group is not None
            and request.user.group.admin_group is not None
        ):
            if request.user.group.territories.all().exists():
                allowed_communes = [
                    x
                    for x in request.user.group.territories.all().values_list(
                        "pk", flat=True
                    )
                    if x
                    in request.user.group.admin_group.territories.all().values_list(
                        "pk", flat=True
                    )
                ]
            else:
                allowed_communes = list(
                    request.user.group.admin_group.territories.all().values_list(
                        "pk", flat=True
                    )
                )

            communes = communes.filter(pk__in=allowed_communes)

        d_epcis = {}
        for commune in communes:
            if commune["epci__pk"] not in d_epcis:
                d_epcis[commune["epci__pk"]] = {
                    "label": commune["epci__name"],
                    "value": commune["epci__pk"],
                    "children": [
                        {"label": commune["name"], "value": commune["pk"]}  # NOQA: E231
                    ],
                }
            else:
                d_epcis[commune["epci__pk"]]["children"].append(
                    {"label": commune["name"], "value": commune["pk"]}  # NOQA: E231
                )

        data = [
            {
                "label": region["name"],
                "value": region["pk"],
                "children": [
                    {
                        "label": departement["name"],
                        "value": departement["pk"],
                        "children": [
                            {
                                "label": epci["name"],
                                "value": epci["pk"],
                                "children": d_epcis[epci["pk"]]["children"],
                            }
                            for epci in epcis
                            if epci["commune__departement"] == departement["pk"]
                            and epci["pk"] in d_epcis
                        ],
                    }
                    for departement in departements
                    if departement["region__pk"] == region["pk"]
                ],
            }
            for region in regions
        ]

        # Add towns without EPCI
        towns_without_epci = Commune.objects.filter(epci=None)
        if (
            "allowed" in request.GET
            and not request.user.is_anonymous
            and request.user.group is not None
            and request.user.group.admin_group is not None
        ):
            towns_without_epci = towns_without_epci.filter(
                pk__in=request.user.group.admin_group.territories.all()
            )

        for commune in towns_without_epci:
            region_pk = commune.departement.region.pk
            departement_pk = commune.departement.pk
            for region_index in range(len(data)):
                if data[region_index]["value"] == region_pk:
                    for departement_index in range(len(data[region_index]["children"])):
                        if (
                            data[region_index]["children"][departement_index]["value"]
                            == departement_pk
                        ):
                            data[region_index]["children"][departement_index][
                                "children"
                            ].append(
                                {
                                    "label": commune.name,
                                    "value": commune.pk,
                                }  # NOQA: E231
                            )
                            break
                    break

        # clean orphans if needed
        if "allowed" in request.GET:
            for i_region in range(len(data) - 1, -1, -1):
                for i_dep in range(len(data[i_region]["children"]) - 1, -1, -1):
                    for i_epci in range(
                        len(data[i_region]["children"][i_dep]["children"]) - 1, -1, -1
                    ):
                        if (
                            "children"
                            in data[i_region]["children"][i_dep]["children"][i_epci]
                            and data[i_region]["children"][i_dep]["children"][i_epci][
                                "children"
                            ]
                            == []
                        ):
                            data[i_region]["children"][i_dep]["children"].pop(i_epci)
                    if data[i_region]["children"][i_dep]["children"] == []:
                        data[i_region]["children"].pop(i_dep)
                if data[i_region]["children"] == []:
                    data.pop(i_region)

        return JsonResponse(data, safe=False)
