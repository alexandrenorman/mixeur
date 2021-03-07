# -*- coding: utf-8 -*-
# from django.shortcuts import get_object_or_404
from helpers.views import AdvisorRequiredApiView, ModelView

# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from dialogwatt.models import CalendarPermanentUrl
from dialogwatt.forms import CalendarPermanentUrlForm
from dialogwatt.serializers import CalendarPermanentUrlSerializer

import json


class CalendarPermanentUrlView(ModelView, AdvisorRequiredApiView):
    """
    """

    model = CalendarPermanentUrl
    form = CalendarPermanentUrlForm
    serializer = CalendarPermanentUrlSerializer
    perm_module = "dialogwatt/calendarpermanenturl"

    def post(self, request, *args, **kwargs):
        """
        Create model by [pk]
        """
        object_data = json.loads(request.body)

        form = self.get_form(request, "POST", object_data)(object_data)
        if form.is_valid():
            if "advisors" in object_data and object_data["advisors"]:
                advisors_id = object_data["advisors"]
                advisors_id.sort()
            else:
                raise ValidationError("Le filtre doit contenir au moins un conseiller.")

            if "places" in object_data and object_data["places"]:
                places_id = object_data["places"]
                places_id.sort()
            else:
                raise ValidationError("Le filtre doit contenir au moins un lieu.")

            if "reasons" in object_data and object_data["reasons"]:
                reasons_id = object_data["reasons"]
                reasons_id.sort()
            else:
                raise ValidationError(
                    "Le filtre doit contenir au moins un motif de rendez-vous."
                )

            for object in self.model.objects.filter(user=form.cleaned_data["user"]):
                obj_advisors = [x.pk for x in object.advisors.all()]
                obj_advisors.sort()
                obj_places = [x.pk for x in object.places.all()]
                obj_places.sort()
                obj_reasons = [x.pk for x in object.reasons.all()]
                obj_reasons.sort()

                if (
                    obj_places == places_id
                    and obj_reasons == reasons_id
                    and obj_advisors == advisors_id
                ):
                    return self.get(request, pk=object.pk)

        return super().post(request, *args, **kwargs)

    def post_save(self, request, instance, instance_data, created):

        if "advisors" in instance_data and instance_data["advisors"]:
            advisors_id = instance_data["advisors"]
            instance.advisors.clear()
            instance.advisors.add(*advisors_id)
        else:
            raise ValidationError("Le filtre doit contenir au moins un conseiller.")

        if "places" in instance_data and instance_data["places"]:
            places_id = instance_data["places"]
            instance.places.clear()
            instance.places.add(*places_id)
        else:
            raise ValidationError("Le filtre doit contenir au moins un lieu.")

        if "reasons" in instance_data and instance_data["reasons"]:
            reasons_id = instance_data["reasons"]
            instance.reasons.clear()
            instance.reasons.add(*reasons_id)
        else:
            raise ValidationError(
                "Le filtre doit contenir au moins un motif de rendez-vous."
            )
