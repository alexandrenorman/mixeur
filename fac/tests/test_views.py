import io
from zipfile import ZipFile

from accounts.tests import GroupFactory, UserFactory
from django.test import TestCase, Client
from django.urls import reverse
from fac.models import (
    Contact,
    File,
    Folder,
    MemberOfOrganization,
    Note,
    Organization,
    RelationBetweenOrganization,
)

from .factories import (
    BudgetFactory,
    ContactFactory,
    ListFactory,
    MemberOfOrganizationFactory,
    ObjectiveActionFactory,
    ObjectiveStatusFactory,
    OrganizationFactory,
    PeriodFactory,
    RelationBetweenOrganizationFactory,
    TagFactory,
    FileActionFactory,
    ActionFactory,
)

from .test_fap import InitFapModelMixin


class ViewTestMixin:
    def setUp(self):
        self.anonymous_client = Client()
        self.advisor_client = Client()
        self.user_group = GroupFactory()
        self.advisor = UserFactory(user_type="advisor", group=self.user_group)
        assert self.advisor_client.login(
            username=self.advisor.email, password="password"
        )


class TagViewTestCase(ViewTestMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.other_group = GroupFactory()
        self.visible_tab = TagFactory(owning_group=self.user_group)
        self.invisible_tag = TagFactory(owning_group=self.other_group)

    def test_tag_view_403(self):
        response = self.anonymous_client.get(reverse("fac:tag_list"))
        self.assertEqual(response.status_code, 403)

    def test_tag_view_403_wrong_group(self):
        response = self.advisor_client.get(
            reverse("fac:tag_detail", kwargs={"pk": self.invisible_tag.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_tag_view_200(self):
        response = self.advisor_client.get(
            reverse("fac:tag_detail", kwargs={"pk": self.visible_tab.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], self.visible_tab.pk)
        self.assertIn("contacts", response.json())

    def test_tag_view_list_simple_serializer(self):
        response = self.advisor_client.get(reverse("fac:tag_list"))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("contacts", response.json()[0])


class OrganizationViewTestCase(ViewTestMixin, TestCase):
    def test_is_creating_m2m_relations(self):
        tags = [
            {"label": tag.name, "value": tag.pk} for tag in [TagFactory(), TagFactory()]
        ]
        referent = UserFactory(user_type="advisor", group=self.user_group)
        referents = [
            {"label": ref.full_name, "value": ref.pk}
            for ref in [referent, self.advisor]
        ]
        response = self.advisor_client.post(
            reverse("fac:organization_list"),
            data={
                "owning_group": self.user_group.pk,
                "type_of_organization": "AgenceImmobiliere",
                "name": "mon orga",
                "tags": tags,
                "referents": referents,
                "address": "2, rue de la bonne humeur",
                "lat": 0,
                "lon": 0,
            },
            format="json",
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 200)
        created_organization = Organization.objects.all()[0]
        self.assertEquals(
            {referent.pk for referent in created_organization.referents.all()},
            {referent["value"] for referent in referents},
        )
        self.assertEquals(
            {tag.pk for tag in created_organization.tags.all()},
            {tag["value"] for tag in tags},
        )

    def test_organization_view_list_csv_serializer(self):
        response = self.advisor_client.get(reverse("fac:organization_list") + "?csv=1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("csv" in response.json())


class ContactViewTestCase(ViewTestMixin, TestCase):
    def test_is_creating_m2m_relations(self):
        tags = [
            {"label": tag.name, "value": tag.pk} for tag in [TagFactory(), TagFactory()]
        ]
        response = self.advisor_client.post(
            reverse("fac:contact_list"),
            data={
                "owning_group": self.user_group.pk,
                "civility": "-",
                "first_name": "Rodrigo",
                "last_name": "Del Testo",
                "email": "toto@hespul.org",
                "tags": tags,
                "lat": 0,
                "lon": 0,
            },
            format="json",
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 200)
        created_contact = Contact.objects.all()[0]
        self.assertEquals(
            {tag.pk for tag in created_contact.tags.all()},
            {tag["value"] for tag in tags},
        )

    def test_contact_view_list_simple_serializer(self):
        client = UserFactory(user_type="client", group=self.user_group)
        ContactFactory(owning_group=self.user_group, client_account=client)
        response = self.advisor_client.get(reverse("fac:contact_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.json()[0]["client_account"], client.pk)

    def test_contact_view_list_csv_serializer(self):
        response = self.advisor_client.get(reverse("fac:contact_list") + "?csv=1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("csv" in response.json())

    def test_create_contact_with_client_user(self):
        client = UserFactory(user_type="client", group=self.user_group)
        response = self.advisor_client.post(
            reverse("fac:contact_list"),
            data={
                "owning_group": self.user_group.pk,
                "first_name": "Rodrigo",
                "last_name": "Del Testo",
                "email": "toto@hespul.org",
                "civility": "-",
                "client_account": client.pk,
                "lat": 0,
                "lon": 0,
            },
            format="json",
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 200)
        created_contact = Contact.objects.all()[0]
        self.assertEquals(created_contact.client_account.pk, client.pk)

    def test_get_contact_with_client_user(self):
        client = UserFactory(user_type="client", group=self.user_group)
        created_contact = ContactFactory(
            owning_group=self.user_group, client_account=client
        )
        response = self.advisor_client.get(
            reverse("fac:contact_detail", kwargs={"pk": created_contact.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.json()["client_account"]["pk"], client.pk)


class NoteViewTestCase(ViewTestMixin, TestCase):
    def test_is_creating_m2m_relations(self):
        tags = [
            {"label": tag.name, "value": tag.pk} for tag in [TagFactory(), TagFactory()]
        ]
        contact = ContactFactory(owning_group=self.user_group)
        response = self.advisor_client.post(
            reverse("fac:note_list"),
            data={
                "owning_group": self.user_group.pk,
                "note": "ma note",
                "tags": tags,
                "linked_object": {"pk": contact.pk, "type": "contact"},
                "reminder": {
                    "date": "2020-05-08",
                    "persons": [{"value": self.advisor.pk, "label": str(self.advisor)}],
                },
            },
            format="json",
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 200)
        created_note = Note.objects.all()[0]
        self.assertEquals(
            {tag.pk for tag in created_note.tags.all()}, {tag["value"] for tag in tags}
        )

    def test_create_contact_note(self):
        contact = ContactFactory(owning_group=self.user_group)
        response = self.advisor_client.post(
            reverse("fac:note_list"),
            data={
                "owning_group": self.user_group.pk,
                "note": "ma note",
                "tags": [],
                "linked_object": {"pk": contact.pk, "type": "contact"},
                "reminder": {
                    "date": "2020-05-08",
                    "persons": [{"value": self.advisor.pk, "label": str(self.advisor)}],
                },
            },
            format="json",
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 200)
        created_note = Note.objects.all()[0]
        self.assertEquals(created_note.linked_object, contact)
        self.assertEquals(created_note.creator, self.advisor)

    def test_create_organization_note(self):
        organization = OrganizationFactory(owning_group=self.user_group)
        response = self.advisor_client.post(
            reverse("fac:note_list"),
            data={
                "owning_group": self.user_group.pk,
                "note": "ma note",
                "tags": [],
                "linked_object": {"pk": organization.pk, "type": "organization"},
                "reminder": {
                    "date": "2020-05-08",
                    "persons": [{"value": self.advisor.pk, "label": str(self.advisor)}],
                },
            },
            format="json",
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 200)
        created_note = Note.objects.all()[0]
        self.assertEquals(created_note.linked_object, organization)
        self.assertEquals(created_note.creator, self.advisor)


class MemberOfOrganizationViewTestCase(ViewTestMixin, TestCase):
    def test_is_creating_m2m_relations(self):
        tags = [
            {"label": tag.name, "value": tag.pk} for tag in [TagFactory(), TagFactory()]
        ]
        competencies_tags = [
            {"label": tag.name, "value": tag.pk} for tag in [TagFactory(), TagFactory()]
        ]
        contact = ContactFactory(owning_group=self.user_group)
        organization = OrganizationFactory(owning_group=self.user_group)
        response = self.advisor_client.post(
            reverse("fac:member_of_organization_list"),
            data={
                "owning_group": self.user_group.pk,
                "contact": contact.pk,
                "organization": organization.pk,
                "tags": tags,
                "competencies_tags": competencies_tags,
            },
            format="json",
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 200)
        created_member = MemberOfOrganization.objects.all()[0]
        self.assertEquals(
            {tag.pk for tag in created_member.tags.all()},
            {tag["value"] for tag in tags},
        )
        self.assertEquals(
            {tag.pk for tag in created_member.competencies_tags.all()},
            {tag["value"] for tag in competencies_tags},
        )


class FileOrganizationViewTestCase(ViewTestMixin, TestCase):
    def test_is_creating_m2m_relations(self):
        organization = OrganizationFactory(owning_group=self.user_group)
        tags = [
            {"label": tag.name, "value": tag.pk} for tag in [TagFactory(), TagFactory()]
        ]
        response = self.advisor_client.post(
            reverse("fac:file_list"),
            data={
                "owning_group": self.user_group.pk,
                "tags": tags,
                "linked_object": {"pk": organization.pk, "type": "organization"},
                "document": {
                    "file_name": "test.txt",
                    "content": "data:text;base64,c2RrZmpzZGprZm5zCmRmc2RpZnNrZGZzZGYK",
                },
                "note": "note",
            },
            format="json",
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 200)
        created_file = File.objects.all()[0]
        self.assertEquals(
            {tag.pk for tag in created_file.tags.all()}, {tag["value"] for tag in tags}
        )


class FileContactViewTestCase(ViewTestMixin, TestCase):
    def test_is_creating_m2m_relations(self):
        contact = ContactFactory(owning_group=self.user_group)
        tags = [
            {"label": tag.name, "value": tag.pk} for tag in [TagFactory(), TagFactory()]
        ]
        response = self.advisor_client.post(
            reverse("fac:file_list"),
            data={
                "owning_group": self.user_group.pk,
                "tags": tags,
                "linked_object": {"pk": contact.pk, "type": "contact"},
                "document": {
                    "file_name": "test.txt",
                    "content": "data:text;base64,c2RrZmpzZGprZm5zCmRmc2RpZnNrZGZzZGYK",
                },
                "note": "ma note",
            },
            format="json",
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 200)
        created_file = File.objects.all()[0]
        self.assertEquals(
            {tag.pk for tag in created_file.tags.all()}, {tag["value"] for tag in tags}
        )


class FileZipTestCase(ViewTestMixin, TestCase):
    def test_is_downloading_files_in_zip_format(self):
        action = ActionFactory()
        f = FileActionFactory(
            document__data=b"some text",
            document__filename="some_file.txt",
            linked_object=action,
            owning_group=self.user_group,
        )
        response = self.advisor_client.get(
            reverse("fac:file_list") + f"?zip=1&files={f.pk}"
        )
        with ZipFile(io.BytesIO(response.content)) as zipf:
            with zipf.open("some_file.txt") as some_file:
                self.assertEquals(b"some text", some_file.read())

    def test_is_downloading_files_for_laureates(self):
        action = ActionFactory()
        other_group = GroupFactory()
        other_group.pilot_groups.add(self.user_group)
        f = FileActionFactory(
            document__data=b"some text",
            document__filename="some_file.txt",
            linked_object=action,
            owning_group=other_group,
        )
        response = self.advisor_client.get(
            reverse("fac:file_list") + f"?zip=1&files={f.pk}"
        )
        with ZipFile(io.BytesIO(response.content)) as zipf:
            with zipf.open("some_file.txt") as some_file:
                self.assertEquals(b"some text", some_file.read())

    def test_is_not_downloading_files_for_other_groups(self):
        action = ActionFactory()
        other_group = GroupFactory()
        f = FileActionFactory(
            document__data=b"some text",
            document__filename="some_file.txt",
            linked_object=action,
            owning_group=other_group,
        )
        response = self.advisor_client.get(
            reverse("fac:file_list") + f"?zip=1&files={f.pk}"
        )
        with ZipFile(io.BytesIO(response.content)) as zipf:
            self.assertEquals(0, len(zipf.namelist()))


class RelationBetweenOrganizationViewTestCase(ViewTestMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.organization1 = OrganizationFactory(
            name="Orga1", owning_group=self.user_group
        )
        self.organization2 = OrganizationFactory(
            name="Orga2", owning_group=self.user_group
        )
        self.other_group = GroupFactory()
        self.visible_relation = RelationBetweenOrganizationFactory(
            owning_group=self.user_group,
            first_organization=self.organization1,
            second_organization=self.organization2,
            relation_name="une filiale",
        )
        self.invisible_relation = RelationBetweenOrganizationFactory(
            owning_group=self.other_group
        )

    def test_create_relation(self):
        self.assertEquals(RelationBetweenOrganization.objects.count(), 2)
        response = self.advisor_client.post(
            reverse("fac:relation_between_organization_list"),
            data={
                "owning_group": self.user_group.pk,
                "first_organization": self.organization1.pk,
                "relation_name": "la maison mère",
                "second_organization": self.organization2.pk,
            },
            format="json",
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(RelationBetweenOrganization.objects.count(), 3)
        created_relation = RelationBetweenOrganization.objects.all().order_by("id")[2]
        self.assertEquals(created_relation.first_organization.pk, self.organization1.pk)

    def test_relation_view_403(self):
        response = self.anonymous_client.get(
            reverse("fac:relation_between_organization_list")
        )
        self.assertEqual(response.status_code, 403)

    def test_relation_view_403_wrong_group(self):
        response = self.advisor_client.get(
            reverse(
                "fac:relation_between_organization_detail",
                kwargs={"pk": self.invisible_relation.pk},
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_get_relation(self):
        response = self.advisor_client.get(
            reverse(
                "fac:relation_between_organization_detail",
                kwargs={"pk": self.visible_relation.pk},
            )
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response.json()["display_name"], "Orga1 est une filiale de Orga2"
        )


class FolderModelViewTestCase(InitFapModelMixin, TestCase):
    def test_create_folder_model(self):
        response = self.advisor_client.post(
            reverse("fac:folder_model_list"),
            data={"name": "Dossier Modèle", "project": self.project.pk},
            format="json",
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 403)

    def test_list_folder_models(self):
        response = self.advisor_client.get(
            reverse("fac:folder_model_list"),
            data={"name": "Dossier Modèle", "project": self.project.pk},
            format="json",
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()), 1)


class FolderViewTestCase(InitFapModelMixin, TestCase):
    def test_create_contact_folder(self):
        contact = ContactFactory(owning_group=self.user_group)
        response = self.advisor_client.post(
            reverse("fac:folder_list"),
            data={
                "owning_group": self.user_group.pk,
                "description": "mon projet",
                "model": self.folder_model.pk,
                "linked_object": {"pk": contact.pk, "type": "contact"},
            },
            format="json",
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 200)
        created_folder = Folder.objects.last()
        self.assertEquals(created_folder.linked_object, contact)
        self.assertEquals(created_folder.model.pk, self.folder_model.pk)
        self.assertEquals(
            created_folder.type_valorization.pk, self.type_valorization_1.pk
        )

    def test_create_organization_folder(self):
        self.organization = OrganizationFactory(owning_group=self.user_group)
        response = self.advisor_client.post(
            reverse("fac:folder_list"),
            data={
                "owning_group": self.user_group.pk,
                "description": "mon projet",
                "model": self.folder_model.pk,
                "linked_object": {"pk": self.organization.pk, "type": "organization"},
            },
            format="json",
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 200)
        created_folder = Folder.objects.last()
        self.assertEquals(created_folder.linked_object.pk, self.organization.pk)
        self.assertEquals(created_folder.model.pk, self.folder_model.pk)
        self.assertEquals(
            created_folder.type_valorization.pk, self.type_valorization_1.pk
        )


class ListViewTestCase(ViewTestMixin, TestCase):
    def test_is_creating_m2m_relations(self):
        tags = [
            {"name": tag.name, "pk": tag.pk} for tag in [TagFactory(), TagFactory()]
        ]
        contacts = [
            {"name": contact.full_name, "pk": contact.pk}
            for contact in [
                ContactFactory(owning_group=self.user_group),
                ContactFactory(owning_group=self.user_group),
            ]
        ]
        organizations = [
            {"name": organization.name, "pk": organization.pk}
            for organization in [OrganizationFactory(owning_group=self.user_group)]
        ]

        lists = [
            {"name": lf.title, "pk": lf.pk}
            for lf in [ListFactory(owning_group=self.user_group)]
        ]
        response = self.advisor_client.post(
            reverse("fac:list_list"),
            data={
                "owning_group": self.user_group.pk,
                "tags": tags,
                "contacts": contacts,
                "organizations": organizations,
                "lists": lists,
            },
            format="json",
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 200)

    def test_get_list_list(self):
        ListFactory(owning_group=self.user_group),
        ListFactory(owning_group=self.user_group)

        response = self.advisor_client.get(reverse("fac:list_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_get_contacts(self):
        tag = TagFactory()
        contact_with_tag = ContactFactory(owning_group=self.user_group)
        contact_with_tag.tags.set([tag])

        organization_with_tag = OrganizationFactory(owning_group=self.user_group)
        organization_with_tag.tags.set([tag])

        contact = ContactFactory(owning_group=self.user_group)
        organization = OrganizationFactory(owning_group=self.user_group)

        contact_from_organization = ContactFactory(owning_group=self.user_group)

        # Linkg the contact and the organization
        MemberOfOrganizationFactory(
            owning_group=self.user_group,
            contact=contact_from_organization,
            organization=organization,
        )

        contact_from_sublist = ContactFactory(owning_group=self.user_group)

        organization_from_sublist = OrganizationFactory(owning_group=self.user_group)

        contact_member_from_sublist = ContactFactory(owning_group=self.user_group)

        # Linkg the contact and the organization
        MemberOfOrganizationFactory(
            owning_group=self.user_group,
            contact=contact_member_from_sublist,
            organization=organization_from_sublist,
        )

        sublist = ListFactory(
            owning_group=self.user_group, use_organizations_as_contacts=False
        )
        sublist.contacts.set([contact_from_sublist])
        sublist.organizations.set([organization_from_sublist])

        list_to_check = ListFactory(
            owning_group=self.user_group, use_organizations_as_contacts=True
        )

        list_to_check.tags.set([tag])
        list_to_check.contacts.set([contact])
        list_to_check.organizations.set([organization])
        list_to_check.lists.set([sublist])

        contacts_from_list = list_to_check.get_contacts()
        self.assertIn(contact_with_tag, contacts_from_list)
        self.assertIn(organization_with_tag, contacts_from_list)
        self.assertIn(contact, contacts_from_list)
        self.assertIn(organization, contacts_from_list)
        self.assertNotIn(contact_from_organization, contacts_from_list)
        self.assertNotIn(organization_from_sublist, contacts_from_list)

        self.assertIn(contact_member_from_sublist, contacts_from_list)

        list_to_check.use_organizations_as_contacts = False
        list_to_check.save()

        contacts_from_list = list_to_check.get_contacts()
        self.assertIn(contact_from_organization, contacts_from_list)
        self.assertNotIn(organization, contacts_from_list)
        self.assertNotIn(organization_from_sublist, contacts_from_list)
        self.assertIn(contact_member_from_sublist, contacts_from_list)

    def test_get_contacts_recursive(self):
        contact = ContactFactory(owning_group=self.user_group)
        contact_from_sublist = ContactFactory(owning_group=self.user_group)

        sublist = ListFactory(owning_group=self.user_group)
        sublist.contacts.set([contact_from_sublist])

        list_to_check = ListFactory(owning_group=self.user_group)
        list_to_check.contacts.set([contact])

        list_to_check.lists.set([sublist])
        sublist.lists.set([list_to_check])

        contacts_from_list = list_to_check.get_contacts()
        self.assertIn(contact, contacts_from_list)
        self.assertIn(contact_from_sublist, contacts_from_list)

        contacts_from_sublist = sublist.get_contacts()
        self.assertIn(contact, contacts_from_sublist)
        self.assertIn(contact_from_sublist, contacts_from_sublist)

    def test_get_csv(self):
        list_to_export = ListFactory(
            owning_group=self.user_group, use_organizations_as_contacts=True
        )
        contact = ContactFactory(owning_group=self.user_group)
        organization = OrganizationFactory(
            owning_group=self.user_group, email="test@test.mail"
        )

        list_to_export.contacts.set([contact])
        list_to_export.organizations.set([organization])

        response = self.advisor_client.get(
            reverse("fac:list_detail", kwargs={"pk": list_to_export.pk}) + "?csv=1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(contact.email, response.json()["csv"])
        self.assertIn(organization.email, response.json()["csv"])


class ProjectViewTestCase(InitFapModelMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.period2 = PeriodFactory()

        BudgetFactory(group=GroupFactory(), project=self.project, period=self.period)
        BudgetFactory(group=self.user_group, project=self.project, period=self.period2)

        self.objs1 = ObjectiveStatusFactory(
            period=self.period,
            group=self.user_group,
            status=self.status_1,
            nb_statuses=4,
        )
        self.objs2 = ObjectiveStatusFactory(
            period=self.period2,
            group=GroupFactory(),
            status=self.status_2,
            nb_statuses=1,
        )

        self.action_1.valorization = self.valorization_1
        self.action_2.valorization = self.valorization_2
        self.action_3.valorization = self.valorization_3
        self.type_valorization_1.groups.add(self.user_group)
        self.type_valorization_2.groups.add(self.user_group)
        self.type_valorization_3.groups.add(self.user_group)

        self.action_1.done = True
        self.action_2.done = True
        self.action_3.done = True

        self.action_1.date = self.period.date_start
        self.action_2.date = self.period.date_start
        self.action_3.date = self.period.date_start

        self.action_1.save()
        self.action_2.save()
        self.action_3.save()

        self.obja1 = ObjectiveActionFactory(
            period=self.period,
            group=self.user_group,
            model_action=self.action_model_1,
            nb_actions=98,
        )
        self.obja2 = ObjectiveActionFactory(
            period=self.period2,
            group=self.user_group,
            model_action=self.action_model_2,
            nb_actions=182,
        )
        self.obja3 = ObjectiveActionFactory(
            period=self.period,
            group=self.user_group,
            model_action=self.action_model_3,
            nb_actions=173,
        )

    def test_acl_periods(self):
        response = self.advisor_client.get(reverse("fac:project_list"))
        self.assertEquals(
            {self.period.pk, self.period2.pk},
            {period["pk"] for period in response.json()[0]["periods"]},
        )

    def test_statistics(self):
        date_start = self.period.date_start.strftime("%Y-%m-%d")
        date_end = self.period.date_end.strftime("%Y-%m-%d")
        response = self.advisor_client.get(
            reverse("fac:project_detail", kwargs={"pk": self.project.pk})
            + f"?period={self.period.pk}&date_start={date_start}&date_end={date_end}"
        ).json()
        folder_model_response = response["folder_models"][str(self.folder_model.pk)]
        self.assertTrue(folder_model_response["has_status_objectives"])
        self.assertTrue("categories" in folder_model_response)
        self.assertTrue("statuses" in folder_model_response)
        self.assertEquals(
            {
                "name",
                "total_actions",
                "actions",
                "objective",
                "progression",
                "total_expenses",
            },
            set(folder_model_response["categories"][0].keys()),
        )
        self.assertEquals(
            {
                "name",
                "total",
                "objective",
                "progression",
                "unit_valorisation",
                "is_act",
                "total_valorisation",
                "type_valorizations",
                "quantity",
                "actions_with_files",
            },
            set(folder_model_response["categories"][0]["actions"][0].keys()),
        )
        self.assertEquals(
            {
                "pk",
                "name",
                "nb_status",
                "percentage_nb_organizations",
                "nb_cumulated",
                "objective",
                "progression",
            },
            set(folder_model_response["statuses"][0].keys()),
        )

        self.assertEqual(
            folder_model_response["categories"][0]["actions"][0]["total"], 1
        )
        self.assertEqual(
            folder_model_response["categories"][0]["actions"][1]["total"], 1
        )
        self.assertEqual(
            folder_model_response["categories"][0]["actions"][2]["total"], 1
        )

        self.assertEqual(
            folder_model_response["categories"][0]["actions"][0]["objective"], 98
        )
        self.assertEqual(
            # objective not on the period -> 0
            folder_model_response["categories"][0]["actions"][1]["objective"],
            0,
        )
        self.assertEqual(
            folder_model_response["categories"][0]["actions"][2]["objective"], 173
        )


class StatusViewTestCase(InitFapModelMixin, TestCase):
    def test_status_detail(self):
        date_end = self.period.date_end.strftime("%Y-%m-%d")
        response = self.advisor_client.get(
            reverse("fac:status_detail", kwargs={"pk": self.status_1.pk})
            + f"?date_end={date_end}"
        ).json()
        self.assertEquals(self.status_1.name, response["name"])
        self.assertEquals(
            f"{self.contact.last_name} {self.contact.first_name}",
            response["contactables_with_this_status"][0]["name"],
        )
