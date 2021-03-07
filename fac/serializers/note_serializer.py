# -*- coding: utf-8 -*-
from fac.models import Note, Contact, Organization
from helpers.serializers import AutoModelSerializer

from .tag_select_serializer import TagSelectSerializer
from .user_select_serializer import UserSelectSerializer
from .reminder_serializer import ReminderSerializer


class NoteSerializer(AutoModelSerializer):
    model = Note

    exclude = ["content_type", "object_id", "contact", "organization"]

    def get_linked_object(self, obj):
        linked_object = obj.linked_object
        if not linked_object:
            name = "N/A"
        elif obj.content_type.model == "contact":
            name = linked_object.full_name
        else:
            name = linked_object.name
        if type(linked_object) is Contact:
            return {"type": "contact", "pk": obj.object_id, "name": name}
        if type(linked_object) is Organization:
            return {"type": "organization", "pk": obj.object_id, "name": name}
        return ""

    def get_owning_group(self, obj):
        return obj.owning_group.pk

    def get_creator(self, obj):
        if obj.creator:
            return UserSelectSerializer(obj.creator).data

    def get_tags(self, obj):
        return TagSelectSerializer(obj.tags.all(), many=True).data

    def get_reminder(self, obj):
        reminder = obj.reminder.all()
        if reminder.exists():
            return ReminderSerializer(reminder.first()).data
        else:
            return None
