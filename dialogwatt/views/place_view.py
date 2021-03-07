# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from helpers.views import ApiView, ModelView
from helpers.helpers import decode_base64_file

from dialogwatt.models import Place
from dialogwatt.forms import PlaceForm
from dialogwatt.serializers import PlaceSerializer
from accounts.models import Group
from django.core.exceptions import ValidationError


class PlaceView(ModelView, ApiView):
    """
    PlaceView requires authenticated user

    get :model:`dialogwatt.Place`

    """

    model = Place
    form = PlaceForm
    serializer = PlaceSerializer
    perm_module = "dialogwatt/place"

    def get_serializer(self, request, call):
        return self.serializer

    def filter(self, request, queryset):
        allowed_objects = queryset.all()
        if not request.user.is_anonymous and (
            request.user.is_advisor or request.user.is_manager
        ):
            allowed_objects = [
                x
                for x in allowed_objects
                if request.user.has_perm(f"{self.perm_module}.change", x)
            ]
        return allowed_objects

    def post_save(self, request, place, place_data, created):  # NOQA: C901
        """
        Save groups as M2M field
        """
        if "groups" in place_data and place_data["groups"]:
            groups_id = [x["pk"] for x in place_data["groups"]]
            for id in groups_id:
                if place.inseecode in [
                    x.pk for x in get_object_or_404(Group, pk=id).territories.all()
                ]:
                    group = Group.objects.get(pk=id)
                    raise ValueError(f"Group {group.name} {group.pk} not permitted")

            place.groups.clear()
            place.groups.add(*groups_id)
        else:
            raise ValidationError("Le lieu doit être associé à au moins une structure.")

        if "selected_advisors" in place_data and place_data["selected_advisors"]:
            advisors_id = [x["pk"] for x in place_data["selected_advisors"]]
            for id in advisors_id:
                if id not in [x.pk for x in place.advisors]:
                    raise ValueError(f"Advisor {id} not permitted")

            for advisor in place.selected_advisors.filter(
                group=self.request.user.group
            ):
                place.selected_advisors.remove(advisor)

            place.selected_advisors.add(*advisors_id)

        if "img" in place_data:
            if place_data["img"] is None:
                place.img = None
                place.save()
            elif place_data["img"].startswith("data:"):
                place.img = decode_base64_file(place_data["img"])
                place.save()
