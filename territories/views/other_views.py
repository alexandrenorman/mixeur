# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from accounts.models.group import Group

from helpers.views import ApiView, ExpertRequiredApiView, ModelView

from territories.models import Commune, Departement, Epci, Region
from territories.serializers import (
    CommuneSerializer,
    DepartementSerializer,
    EpciSerializer,
    RegionSerializer,
)


def allowed_communes_for_user(user):
    if user.group is None:
        return []
    if user.group.is_admin:
        return user.group.territories.all().order_by("name")
    if user.group.admin_group.is_admin:
        return user.group.admin_group.territories.all().order_by("name")
    return True


def allowed_epcis_for_user(user):
    if user.group is None:
        return []
    if user.group.is_admin or user.group.admin_group.is_admin:
        return Epci.objects.filter(
            pk__in=[
                x["epci"]
                for x in allowed_communes_for_user(user).values("epci").distinct()
            ]
        ).order_by("name")
    return True


def allowed_departements_for_user(user):
    if user.group is None:
        return []
    if user.group.is_admin or user.group.admin_group.is_admin:
        return Departement.objects.filter(
            pk__in=[
                x["departement"]
                for x in allowed_communes_for_user(user)
                .values("departement")
                .distinct()
            ]
        ).order_by("name")
    return True


def allowed_regions_for_user(user):
    if user.group is None:
        return []
    if user.group.is_admin or (
        user.group.admin_group is not None and user.group.admin_group.is_admin
    ):
        return Region.objects.filter(
            pk__in=[
                x["region"]
                for x in allowed_departements_for_user(user).values("region").distinct()
            ]
        ).order_by("name")
    return True


class OtherRegionView(ApiView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous and (
            request.user.is_manager or request.user.is_advisor
        ):
            regions = allowed_regions_for_user(request.user)
        else:
            regions = Region.objects.all().order_by("name")

        serializer = RegionSerializer(regions, many=True)
        return JsonResponse(serializer.data, safe=False)


class OtherDepartementView(ApiView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous and (
            request.user.is_manager or request.user.is_advisor
        ):
            departements = allowed_departements_for_user(request.user)
        else:
            departements = Departement.objects.all().order_by("name")

        if "region_id" in kwargs:
            departements = departements.filter(region__id=kwargs["region_id"]).order_by(
                "name"
            )

        serializer = DepartementSerializer(departements, many=True)
        return JsonResponse(serializer.data, safe=False)


class OtherEpciView(ApiView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous and (
            request.user.is_manager or request.user.is_advisor
        ):
            epcis = allowed_epcis_for_user(request.user)
        else:
            epcis = Epci.objects.all().order_by("name")

        if "departement_id" in kwargs:
            departement = kwargs["departement_id"]
            epcis = epcis.filter(
                pk__in=[
                    x.epci.pk
                    for x in Commune.objects.select_related("epci").filter(
                        departement=departement
                    )
                ]
            ).order_by("name")

        serializer = EpciSerializer(epcis, many=True)
        return JsonResponse(serializer.data, safe=False)


class OtherCommuneView(ApiView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous and (
            request.user.is_manager or request.user.is_advisor
        ):
            communes = allowed_communes_for_user(request.user)
        else:
            communes = Commune.objects.all().order_by("name")

        if "departement_id" in kwargs:
            departement_id = kwargs["departement_id"]
            communes = communes.filter(departement__pk=departement_id).order_by("name")
        elif "epci_id" in kwargs:
            epci_id = kwargs["epci_id"]
            communes = communes.filter(epci__pk=epci_id).order_by("name")
        elif "group_id" in kwargs:
            group_id = kwargs["group_id"]
            group = get_object_or_404(Group, pk=group_id)
            if group.admin_group:
                admin_group = group.admin_group
            elif group.is_admin:
                admin_group = group
            else:
                raise ValueError(f"Unattended group {group_id}")

            allowed_communes = [
                x.pk for x in communes if x in admin_group.territories.all()
            ]

            communes = communes.filter(pk__in=allowed_communes)

        serializer = CommuneSerializer(communes, many=True)
        return JsonResponse(serializer.data, safe=False)


class OtherEpciForGroupView(ModelView, ExpertRequiredApiView):
    """"""

    model = Epci
    form = None
    serializer = EpciSerializer

    def filter(self, request, queryset):  # NOQA: A003
        if "for_group" in request.GET:
            for_group = request.GET["for_group"]
            group = get_object_or_404(Group, pk=for_group)
            epcis = [
                x["epci__pk"]
                for x in group.territories.all().values("epci__pk").distinct()
            ]
            queryset = queryset.filter(pk__in=epcis)

        return queryset
