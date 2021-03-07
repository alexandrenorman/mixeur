from django.test import TestCase

from accounts.tests import GroupFactory, UserFactory
from fac.forms import NoteForm
from fac.tests.factories import ContactFactory, OrganizationFactory


class NoteFormTestCase(TestCase):
    def setUp(self):
        self.group1 = GroupFactory()
        self.group2 = GroupFactory()
        self.contact = ContactFactory(owning_group=self.group1)
        self.advisor = UserFactory(user_type="advisor", group=self.group1)
        self.organization = OrganizationFactory(owning_group=self.group1)

    def test_contact_wrong_owning_group(self):
        data = {
            "note": "something",
            "linked_object": {"pk": self.contact.pk, "type": "contact"},
            "owning_group": self.group2.pk,
            "reminder": {
                "date": "2020-05-08",
                "persons": [{"value": self.advisor.pk, "label": str(self.advisor)}],
            },
        }
        form = NoteForm(data=data)
        form.full_clean()
        self.assertEquals(
            form.errors["__all__"][0], "Le contact n'appartient pas à ce groupe"
        )

    def test_organization_wrong_owning_group(self):
        data = {
            "note": "something",
            "linked_object": {"pk": self.organization.pk, "type": "organization"},
            "owning_group": self.group2.pk,
            "reminder": {
                "date": "2020-05-08",
                "persons": [{"value": self.advisor.pk, "label": str(self.advisor)}],
            },
        }
        form = NoteForm(data=data)
        form.full_clean()
        self.assertEquals(
            form.errors["__all__"][0], "La structure n'appartient pas à ce groupe"
        )

    def test_recurrence_malformed_data(self):
        data = {
            "note": "something",
            "linked_object": {"pk": self.organization.pk, "type": "organization"},
            "owning_group": self.group1.pk,
            "reminder": {
                "recurrences": "wrong_format",
                "persons": [{"value": self.advisor.pk, "label": str(self.advisor)}],
            },
        }
        form = NoteForm(data=data)
        form.full_clean()
        self.assertEquals(form.errors["__all__"][0], "malformed data")

    def test_recurrence_but_no_reminder_persons(self):
        data = {
            "note": "something",
            "linked_object": {"pk": self.organization.pk, "type": "organization"},
            "owning_group": self.group1.pk,
            "reminder": {
                "date": "",
                "persons": [{"value": self.advisor.pk, "label": str(self.advisor)}],
            },
        }
        form = NoteForm(data=data)
        form.full_clean()
        self.assertEquals(
            form.errors["__all__"][0],
            "Veuillez soit sélectionner des personnes à rappeler "
            "ET une date, soit ne rien selectionner",
        )

    def test_reminder_persons_but_no_recurrence(self):
        data = {
            "note": "something",
            "linked_object": {"pk": self.organization.pk, "type": "organization"},
            "owning_group": self.group1.pk,
            "reminder": {"date": "2020-05-08", "persons": []},
        }
        form = NoteForm(data=data)
        form.full_clean()
        self.assertEquals(
            form.errors["__all__"][0],
            "Veuillez soit sélectionner des personnes à rappeler "
            "ET une date, soit ne rien selectionner",
        )

    def test_create_recurrent_note(self):
        data = {
            "note": "something",
            "linked_object": {"pk": self.organization.pk, "type": "organization"},
            "owning_group": self.group1.pk,
            "reminder": {
                "date": "2020-05-08",
                "persons": [{"value": self.advisor.pk, "label": str(self.advisor)}],
            },
        }
        form = NoteForm(data=data)
        form.save()
        self.assertEquals(form.errors, {})
