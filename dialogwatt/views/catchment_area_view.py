# -*- coding: utf-8 -*-
# from django.shortcuts import get_object_or_404
from helpers.views import ModelView, ExpertRequiredApiView

from dialogwatt.models import CatchmentArea
from dialogwatt.forms import CatchmentAreaForm
from dialogwatt.serializers import CatchmentAreaSerializer
from territories.models import Commune
from django.core.exceptions import ValidationError


class CatchmentAreaView(ModelView, ExpertRequiredApiView):
    """
    CatchmentAreaView requires authenticated user

    get :model:`dialogwatt.CatchmentArea`

    """

    model = CatchmentArea
    form = CatchmentAreaForm
    serializer = CatchmentAreaSerializer
    perm_module = "dialogwatt/catchment_area"

    def post_save(self, request, catchment_area, catchment_area_data, created):
        """
        Save territories as M2M field
        """
        if "territories" in catchment_area_data and catchment_area_data["territories"]:
            # territories_id = [x["pk"] for x in catchment_area_data["territories"]]
            territories_id = catchment_area_data["territories"]
            for id in territories_id:
                try:
                    commune = Commune.objects.get(pk=id)
                except Exception:
                    raise ValidationError(f"La commune {id} n'existe pas.")

                if not self.request.user.has_perm("commune.can_use", commune):
                    raise ValueError(
                        f"Vous n'avez pas la permission d'utiliser la commune {commune.name} / {commune.pk}"
                    )

            catchment_area.territories.clear()
            catchment_area.territories.add(*territories_id)
        else:
            raise ValidationError(
                "La zone de chalandise doit être associée à au moins une commune."
            )
