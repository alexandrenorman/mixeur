# -*- coding: utf-8 -*-

from django.http import JsonResponse

from rest_framework import status

from custom_forms.models import CustomForm
from custom_forms.serializers import CustomFormSerializer

from helpers.views import ExpertRequiredApiView, ModelReadOnlyView, PreventListViewMixin


class CustomFormView(PreventListViewMixin, ModelReadOnlyView, ExpertRequiredApiView):
    """
    CustomView requires authenticated user
    """

    model = CustomForm
    form = None
    serializer = CustomFormSerializer
    perm_module = None

    def get(self, request, *args, **kwargs):
        """
        Get model by [pk]
        """
        model = kwargs["model"]
        anchor = kwargs["anchor"]

        group_pk = None
        project_pk = None
        folder_model_pk = None
        action_model_pk = None

        if "group" in request.GET:
            group_pk = request.GET["group"]

        if "project" in request.GET:
            project_pk = request.GET["project"]

        if "folder_model" in request.GET:
            folder_model_pk = request.GET["folder_model"]

        if "action_model" in request.GET:
            action_model_pk = request.GET["action_model"]

        if (
            group_pk is None
            and project_pk is None
            and folder_model_pk is None
            and action_model_pk is None
        ):
            return JsonResponse(
                {
                    "error": "view not permitted. Must provide ActionModel, FolderModel, Group or Project"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        obj = (
            self.model.objects.filter(
                model=model,
                anchor=anchor,
                folder_models__pk=folder_model_pk,
                action_models__pk=action_model_pk,
                groups__pk=group_pk,
                projects__pk=project_pk,
            )
            .order_by("-version")
            .first()
        )
        if obj is None:
            return JsonResponse(
                {"error": "object not found"}, status=status.HTTP_404_NOT_FOUND
            )

        perm = self.get_perm_module(request, "GET")
        if perm and not request.user.has_perm(f"{perm}.view", obj):
            return JsonResponse(
                {"error": "view not permitted"}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(request, "GET")(obj)
        return JsonResponse(serializer.data)
