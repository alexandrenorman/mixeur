# -*- coding: utf-8 -*-
import json

from django.db import IntegrityError, transaction
from django.http import JsonResponse

from rest_framework import status

from accounts.forms import GroupForm, GroupPartialForm
from accounts.models import Group
from accounts.serializers import GroupSerializer

from helpers.views import ExpertRequiredApiView, ModelReadOnlyView, ModelView

from territories.models import Commune


class GroupAdminView(ExpertRequiredApiView, ModelView):
    perm_module = "group_place"

    def get(self, request, *args, **kwargs):
        groups = Group.objects.filter(is_admin=True)
        serializer = GroupSerializer(groups, many=True)
        return JsonResponse(serializer.data, safe=False)


class PilotLaureateGroupView(ModelReadOnlyView, ExpertRequiredApiView):
    def get(self, request, *args, **kwargs):
        if not request.user.group:
            return JsonResponse({})

        group = Group.objects.get(pk=request.user.group.pk)
        serializer = GroupSerializer(group)
        return JsonResponse(serializer.data)


class GroupView(ExpertRequiredApiView, ModelView):
    model = Group
    serializer = GroupSerializer
    perm_module = "accounts/group"

    def filter(self, request, queryset):  # NOQA: A003
        if "inseecode" in request.GET:
            queryset = queryset.filter(
                territories__inseecode=request.GET["inseecode"], is_admin=False
            )

        return queryset.select_related("admin_group").prefetch_related("territories")

    def pre_delete(self, instance):
        for user in instance.users:
            user.delete()

    def get_perm_module(self, request, call):
        if "inseecode" in request.GET:
            return "group_place"

        return super().get_perm_module(request, call)

    def get_form(self, request, call, instance_data):
        if self.request.user.is_administrator or self.request.user.is_manager:
            return GroupForm

        return GroupPartialForm

    def patch(self, request, *args, **kwargs):  # NOQA C901
        """
        Update model by [pk]

        Must have model.change permission
        """
        try:
            key = kwargs["pk"]
        except KeyError:
            return JsonResponse(
                {"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        object_data = json.loads(request.body)

        pk = key
        try:
            obj = self.model.objects.get(pk=pk)
        except Exception:
            return JsonResponse(
                {"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        if self.perm_module:
            if not (
                request.user.has_perm(f"{self.perm_module}.change", obj)
                or request.user.has_perm(f"{self.perm_module}.partial_change", obj)
            ):
                return JsonResponse(
                    {"error": "change not permitted"}, status=status.HTTP_403_FORBIDDEN
                )

        form = self.get_form(request, "PATCH", object_data)(object_data, instance=obj)
        if form.is_valid():
            message = ""
            try:
                with transaction.atomic():
                    form.save()
                    try:
                        self.post_save(request, obj, object_data, False)
                    except Exception as e:
                        message = str(e)
                        raise IntegrityError

            except IntegrityError:
                return JsonResponse(
                    {"__all__": [message]}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

        return self.get(request, pk=obj.pk)

    def post_save(self, request, group, group_data, created):

        if self.request.user.has_perm("group.change", group):
            if "territories" in group_data:
                territories_id = group_data["territories"]

                if self.request.user.is_manager:
                    for commune in Commune.objects.filter(pk__in=territories_id):
                        if commune not in self.request.user.group.territories.all():
                            raise ValueError(
                                f"Commune {commune.name} {commune.pk} not permitted"
                            )

                group.territories.clear()
                group.territories.add(*territories_id)
