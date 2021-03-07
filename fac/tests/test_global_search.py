from accounts.tests import UserFactory, GroupFactory
from django.test import TestCase, Client
from django.urls import reverse
from fac.tests.factories import ContactFactory, OrganizationFactory


class GlobalSearchTestCase(TestCase):
    def setUp(self):
        self.anonymous_client = Client()
        self.advisor_client = Client()
        self.group = GroupFactory()
        advisor = UserFactory(user_type="advisor", group=self.group)
        assert self.advisor_client.login(username=advisor.email, password="password")

    def test_global_search_contacts_403(self):
        response = self.anonymous_client.get(reverse("fac:global_search"))
        self.assertEqual(response.status_code, 403)

    def test_global_search_contacts(self):
        contact = ContactFactory(first_name="hello", owning_group=self.group)
        response = self.advisor_client.get(
            reverse("fac:global_search") + "?q={}".format(contact.email)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["contacts"][0]["first_name"], "hello")

    def test_global_search_contacts_fuzzy(self):
        ContactFactory(first_name="hellohowareyou", owning_group=self.group)
        response = self.advisor_client.get(
            reverse("fac:global_search") + "?q=hellohoware"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["contacts"][0]["first_name"], "hellohowareyou")

    def test_global_search_contacts_fuzzy_phone_number(self):
        ContactFactory(first_name="hello", phone="0123456789", owning_group=self.group)
        response = self.advisor_client.get(reverse("fac:global_search") + "?q=23456789")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["contacts"][0]["first_name"], "hello")

    def test_global_search_only_contacts(self):
        ContactFactory(first_name="hello", owning_group=self.group)
        OrganizationFactory(name="hello", owning_group=self.group)
        response = self.advisor_client.get(
            reverse("fac:global_search") + "?q=hello&type=contacts"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["contacts"]), 1)
        self.assertNotIn("organizations", response.json())

    def test_global_search_contacts_and_organizations(self):
        ContactFactory(first_name="hello", owning_group=self.group)
        OrganizationFactory(name="hello", owning_group=self.group)
        response = self.advisor_client.get(reverse("fac:global_search") + "?q=hello")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["contacts"]), 1)
        self.assertEqual(len(response.json()["organizations"]), 1)

    def test_permission_for_contacts_and_organizations(self):
        other_group = GroupFactory()
        contact = ContactFactory(first_name="hello", owning_group=self.group)
        ContactFactory(first_name="hello", owning_group=other_group)
        organization = OrganizationFactory(name="hello1", owning_group=self.group)
        OrganizationFactory(name="hello2", owning_group=other_group)

        response = self.advisor_client.get(reverse("fac:global_search") + "?q=hello")

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json()["contacts"]), 1)
        self.assertEqual(
            response.json()["contacts"][0]["owning_group"], contact.owning_group.pk
        )

        self.assertEqual(len(response.json()["organizations"]), 1)
        self.assertEqual(
            response.json()["organizations"][0]["owning_group"],
            organization.owning_group.pk,
        )
