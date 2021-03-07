from datetime import date, timedelta
from unittest.mock import MagicMock

from django.core.management import call_command
from django.test import TestCase

from accounts.tests import GroupFactory, UserFactory
from .factories import (
    ContactFactory,
    NoteFactory,
    OrganizationFactory,
    ReminderNoteFactory,
    ReminderActionFactory,
)
from .test_fap import InitFapModelMixin


class SendRemindersTestCase(InitFapModelMixin, TestCase):
    def test_send_reminders(self):
        from messaging import tasks

        tasks.background_send_email_to_user = MagicMock(
            name="background_send_email_to_user"
        )

        user_group = GroupFactory()
        advisor = UserFactory(user_type="advisor", group=user_group)
        user = UserFactory(user_type="client", group=user_group)
        contact = ContactFactory(owning_group=user_group)

        yesterday = date.today() - timedelta(1)
        organization = OrganizationFactory(owning_group=user_group)
        note_contact = NoteFactory(linked_object=contact)
        reminder_contact = ReminderNoteFactory(
            linked_object_task=note_contact,
            linked_object_contactable=note_contact.linked_object,
            done=False,
        )
        reminder_contact_action = ReminderActionFactory(
            linked_object_task=self.action_3,
            linked_object_contactable=note_contact.linked_object,
            done=False,
        )
        reminder_contact.persons.set([advisor, user])
        reminder_contact_action.persons.set([advisor, user])

        note_organization = NoteFactory(linked_object=organization)
        reminder_organization = ReminderNoteFactory(
            linked_object_task=note_organization,
            linked_object_contactable=note_organization.linked_object,
            date=yesterday,
            done=False,
        )
        reminder_organization_action = ReminderActionFactory(
            linked_object_task=self.action_3,
            linked_object_contactable=note_organization.linked_object,
            date=yesterday,
            done=False,
        )
        reminder_organization.persons.set([advisor, user])
        reminder_organization_action.persons.set([advisor, user])

        call_command("SendReminders")

        tasks.background_send_email_to_user.assert_called_once()

        self.assertEqual(
            tasks.background_send_email_to_user.call_args[1]["recipient_list"],
            [advisor.email],
        )
        self.assertEqual(
            tasks.background_send_email_to_user.call_args[1]["subject"],
            "mixeur - [FAC] 4 rappels en attente",
        )
        self.assertIn(
            "4 rappels en attente",
            tasks.background_send_email_to_user.call_args[1]["html_message"],
        )
