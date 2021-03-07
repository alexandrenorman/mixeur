# -*- coding: utf-8 -*-
from datetime import datetime

from django import forms

import recurrence

from fac.models import Reminder


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        exclude = ["created_at", "updated_at"]


class ReminderFormMixin:
    def clean_reminder(self, value):
        reminder_persons = value.get("persons")
        new_recurrences = value.get("recurrences")
        new_reminder_date = value.get("date")
        initial_recurrences = None
        reminder = self.instance.reminder.first()
        if reminder:
            initial_recurrences = reminder.recurrences

        if not new_recurrences and not new_reminder_date and not reminder_persons:
            return None

        today = datetime.now().replace(minute=0, hour=0, second=0, microsecond=0)

        if not new_reminder_date and new_recurrences != recurrence.serialize(
            initial_recurrences
        ):
            # recurrences have changed
            next_occurrence = recurrence.deserialize(new_recurrences).after(
                today, inc=True
            )
            value["date"] = datetime.strftime(next_occurrence, "%Y-%m-%d")
            if initial_recurrences:
                # it's an existing reminder
                value["done"] = False

        if "done" in value and value.get("done") and new_recurrences:
            # user has completed the reminder
            reminder_datetime = datetime.strptime(value["date"], "%Y-%m-%d")
            next_occurrence = recurrence.deserialize(new_recurrences).after(
                max(today, reminder_datetime), dtstart=max(today, reminder_datetime)
            )
            if next_occurrence:
                value["done"] = False
                value["date"] = next_occurrence

        return value

    def clean(self):
        self.data["reminder"] = self.clean_reminder(self.data.get("reminder"))
        return super().clean()
