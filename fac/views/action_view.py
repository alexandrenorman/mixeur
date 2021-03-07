# -*- coding: utf-8 -*-
import json
from datetime import date

from django.http import JsonResponse

from fac.forms import ActionForm
from fac.models import Action, Tag, Valorization
from fac.serializers import (
    ActionFolderSerializer,
    ActionSimpleSerializer,
    StatusSimpleSerializer,
)

from helpers.views import ExpertRequiredApiView, ModelView

from .reminder_view import ReminderViewMixin


class ActionView(ReminderViewMixin, ModelView, ExpertRequiredApiView):
    """
    ContactView requires authenticated user

    get :model:`fac.Contact`

    """

    model = Action
    form = ActionForm
    serializer = ActionFolderSerializer
    perm_module = "action"

    def post_save(self, request, action, action_data, created):
        super().post_save(request, action, action_data, created)
        self._save_m2m_from_select(
            instance=action,
            attribute="tags",
            model_queryset=Tag.objects,
            data=action_data.get("tags", []),
        )

    def get_serializer(self, request, call):
        if call == "LIST":
            return ActionSimpleSerializer
        return self.serializer

    def pre_form(self, request, instance_data, created=False, *args, **kwargs):
        instance_data = super().pre_form(
            request, instance_data, created, *args, **kwargs
        )

        today = date.today()
        # Type of valorisation
        valorization = Valorization.objects.filter(
            action_models__pk=instance_data.get("model"),
            type_valorization__folders__pk=instance_data.get("folder"),
            type_valorization__groups=request.user.group,
            period__date_start__lte=today,
            period__date_end__gte=today,
        )

        if valorization.exists():
            instance_data["valorization"] = valorization.first().pk
        if not created:  # There is already an instance of Action\
            action_db = Action.objects.get(pk=instance_data.get("pk"))
            # if the instance is now done and wasn't
            if not action_db.done and instance_data.get("done", False):
                instance_data["done_by"] = self.request.user.pk
            if action_db.done and instance_data.get("done", False):
                instance_data["done_by"] = action_db.done_by.pk
            if not instance_data.get("done", False):  # Reset the done_by
                instance_data["done_by"] = None
        elif instance_data.get("done", False):
            instance_data["done_by"] = self.request.user.pk
        return instance_data

    def pre_delete(self, instance):
        self.action_folder = instance.folder

    def delete(self, request, *args, **kwargs):
        self.action_folder = None
        response = super().delete(request, *args, **kwargs)
        if response.status_code != 200:
            return response

        # action has been deleted
        if self.action_folder:
            status = self.action_folder.get_status()
            if status:
                return JsonResponse(
                    {"folder_status": StatusSimpleSerializer(status).data}
                )
        return response

    def patch(self, request, *args, **kwargs):
        object_data = json.loads(request.body)
        if not object_data.get("do_reset"):
            return super().patch(request, *args, **kwargs)

        # reset the action entirely
        action = Action.objects.get(pk=object_data["pk"])
        action.files.all().delete()
        action.reminder.all().delete()
        new_action = Action(
            pk=action.pk,
            model=action.model,
            created_at=action.created_at,
            folder=action.folder,
            valorization=action.valorization,
        )
        new_action.save()

        return JsonResponse(
            {
                "folder_status": StatusSimpleSerializer(
                    new_action.folder.get_status()
                ).data
            }
        )
