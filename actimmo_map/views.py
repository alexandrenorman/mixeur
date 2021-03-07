# -*- coding: utf-8 -*-
from django.http import JsonResponse

from actimmo_map.models import ActimmoContact, ActimmoMap
from actimmo_map.serializers import ActimmoContactSerializer, ActimmoMapSerializer

from fac.models import Action, FolderModel, Organization, Status
from fac.serializers import OrganizationMapSerializer

from helpers.views import ApiView, ModelReadOnlyView


class ActimmoMapView(ModelReadOnlyView, ApiView):
    model = ActimmoMap
    serializer = ActimmoMapSerializer


class ActimmoContactView(ModelReadOnlyView, ApiView):
    model = ActimmoContact
    serializer = ActimmoContactSerializer


class ActimmoIconsView(ApiView):
    def get(self, request, *args, **kwargs):
        folder_models = FolderModel.objects.filter(
            name__in=[
                "Banque",
                "Agence immobilière",
                "Chambre départementale des notaires",
            ]
        )

        return JsonResponse(
            [
                {"name": f.name, "icon_marker_content": f.icon_marker_content}
                for f in folder_models
            ],
            safe=False,
        )


class ActimmoPartnersView(ApiView):
    def get_partner_status(self):
        return Status.objects.get(pk=10)

    def get_folders(self, group):
        folders = self.get_partner_status().folder_model.folders.filter(
            owning_group=group
        )
        return folders

    def get(self, request, *args, **kwargs):
        organizations_pk = Action.objects.filter(
            model__name__contains="Signature", done=True
        ).values_list("folder__object_id", flat=True)
        serializer = OrganizationMapSerializer(
            Organization.objects.filter(pk__in=organizations_pk)
            .exclude(lat=0, lon=0)
            .distinct(),
            many=True,
        )

        return JsonResponse(serializer.data, safe=False)
