# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType

from helpers.views import ExpertRequiredApiView, ModelReadOnlyView

from accounts.models import User
from fac.models import Reminder
from fac.serializers import ReminderSerializer


class ReminderView(ModelReadOnlyView, ExpertRequiredApiView):
    """
    Reminder View
    """

    model = Reminder
    serializer = ReminderSerializer
    updated_at_attribute_name = "updated_at"
    perm_module = "reminder"

    def filter(self, request, queryset):
        return super().filter(request, queryset).accessible_by(request.user)


class ReminderViewMixin:
    def post_save(self, request, obj, data, created):
        obj_content_type = ContentType.objects.get(
            app_label="fac", model=self.perm_module
        )
        reminders = Reminder.objects.filter(
            content_type_task=obj_content_type, object_id_task=obj.pk
        )
        reminder_data = data.get("reminder")
        if reminder_data:
            persons = reminder_data.pop("persons", [])
            # Edit
            reminder_data.pop("pk", None)

            if reminders.exists():
                reminder = reminders.first()
                Reminder.objects.filter(pk=reminder.pk).update(**reminder_data)
            else:
                reminder = Reminder.objects.create(
                    owning_group=obj.owning_group,
                    linked_object_task=obj,
                    linked_object_contactable=obj.linked_object,
                    **reminder_data
                )
            self._save_m2m_from_select(
                instance=reminder,
                attribute="persons",
                model_queryset=User.advisors,
                data=persons,
            )
        else:
            if reminders.exists():
                reminders.first().delete()
