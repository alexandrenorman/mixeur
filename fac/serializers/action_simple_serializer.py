# -*- coding: utf-8 -*-
import serpy

from fac.models import Action

from helpers.serializers import AutoModelSerializer

from .action_model_serializer import ActionModelSerializer
from .reminder_serializer import ReminderSerializer
from .tag_select_serializer import TagSelectSerializer


class DocumentsSerializer(serpy.Serializer):
    documents = serpy.MethodField()

    def get_documents(self, action):
        return [
            {"pk": file.pk, "name": file.document.name, "url": file.document.url}
            for file in action.files.all()
        ]


class ActionSimpleSerializer(AutoModelSerializer, DocumentsSerializer):
    model = Action

    def get_folder(self, action):
        return action.folder.pk

    def get_model(self, action):
        return ActionModelSerializer(action.model).data

    def get_valorization(self, action):
        if action.valorization:
            return action.valorization.pk
        return None

    def get_done_by(self, action):
        if action.done_by:
            return action.done_by.full_name
        return None

    def get_contact(self, action):
        if action.contact:
            return {"value": action.contact.pk, "label": action.contact.full_name}
        else:
            return None

    def get_reminder(self, action):
        if action.reminder.exists():
            return ReminderSerializer(action.reminder.first()).data
        else:
            return None

    def get_duration(self, action):
        return float(action.duration)

    def get_tags(self, action):
        return TagSelectSerializer(action.tags.all(), many=True).data

    def get_custom_form_data(self, obj):
        if obj.custom_form_data is None:
            return {}

        return obj.custom_form_data
