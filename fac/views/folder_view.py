# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType

from fac.forms import FolderForm
from fac.models import Folder, Action
from fac.serializers import FolderSerializer
from helpers.views import ModelView, ExpertRequiredApiView


class FolderView(ModelView, ExpertRequiredApiView):
    """
    Folder View
    """

    model = Folder
    form = FolderForm
    serializer = FolderSerializer
    perm_module = "folder"

    def filter(self, request, queryset):
        object_id = request.GET.get("objectId")
        linked_object_type = request.GET.get("linkedObjectType")
        if not object_id:
            return Folder.objects.none()
        if not linked_object_type and linked_object_type not in {
            "contact",
            "organization",
        }:
            return Folder.objects.none()

        content_type = ContentType.objects.get(
            app_label="fac", model=linked_object_type
        )
        queryset = queryset.filter(object_id=object_id, content_type=content_type)
        queryset = queryset.prefetch_related(
            "type_valorization",
            "actions__model__category_model",
            "actions__contact",
            "actions__done_by",
            "actions__folder",
            "actions__valorization",
            "actions__reminder",
            "actions__files",
            "actions__model__valorizations__type_valorization",
            "actions__model__trigger_status",
            "actions__model__category_model",
            "model__categories__action_models__valorizations__type_valorization",
            "model__categories__action_models__trigger_status",
            "model__categories__action_models__category_model",
            "model__statuses__action_models",
        )
        return queryset.accessible_by(request.user)

    def post_save(self, request, instance, folder_data, created=False):
        """
        Create Actions from Folder's default actions
        """
        if self.request.method != "POST":
            return

        action_models = [
            action_model
            for category in instance.model.categories.all()
            for action_model in category.action_models.filter(default=True)
        ]

        for action_model in action_models:
            Action.objects.create(
                folder=instance,
                model=action_model,
                valorization=action_model.valorizations.filter(
                    type_valorization=instance.type_valorization
                ).first(),
            )
