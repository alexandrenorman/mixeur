# -*- coding: utf-8 -*-
import recurrence

from helpers.serializers import AutoModelSerializer
from fac.models import Reminder
from .user_select_serializer import UserSelectSerializer


class ReminderSerializer(AutoModelSerializer):
    model = Reminder
    exclude = ["note", "action"]

    def get_owning_group(self, obj):
        """
        get field owning_group of type ForeignKey
        """
        return obj.owning_group.pk

    def get_creator(self, obj):
        """
        get field creator of type ForeignKey
        """
        if obj.creator:
            return obj.creator.pk
        return None

    def get_message(self, obj):
        """
        get field note or message of type ForeignKey
        """
        if obj.content_type_task.model == "note":
            return obj.linked_object_task.note
        return obj.linked_object_task.message

    def get_content_type_task(self, obj):
        """
        get field content_type of type ForeignKey
        """
        return obj.content_type_task.pk

    def get_done(self, obj):
        """
        get field 'done' through linked object
        """
        return obj.done

    def get_content_type_contactable(self, obj):
        """
        get field content_type of type ForeignKey
        """
        return obj.content_type_contactable.pk

    def get_linked_object_contactable(self, obj):
        linked_object = obj.linked_object_contactable
        if not linked_object:
            name = "N/A"
        elif obj.content_type_contactable.model == "contact":
            name = linked_object.full_name
        else:
            name = linked_object.name
        return {
            "type": obj.content_type_contactable.model,
            "pk": obj.object_id_contactable,
            "name": name,
        }

    def get_linked_object_task(self, obj):
        return {"type": obj.content_type_task.model, "pk": obj.object_id_task}

    def get_persons(self, obj):
        return UserSelectSerializer(obj.persons.all(), many=True).data

    def get_recurrences(self, obj):
        return recurrence.serialize(obj.recurrences)
