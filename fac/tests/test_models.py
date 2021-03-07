from accounts.tests.factories import GroupFactory

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from os.path import join, dirname, abspath

from fac.models import (
    Contact,
    MemberOfOrganization,
    find_duplicated_contacts,
    RelationBetweenOrganization,
    FolderModel,
)
from fac.tests.factories import ContactFactory, OrganizationFactory
from .test_fap import InitFapModelMixin

LIST_ADDRESS_ATTR = ["address", "zipcode", "town", "country", "phone", "fax"]
FILES_DIR = join(dirname(abspath(__file__)), "files")


class ContactTestCase(TestCase):
    def setUp(self):
        self.contact = ContactFactory(last_name="Norman")
        ContactFactory(last_name="Normna")

    def test_detect_duplicates_same_contact(self):
        self.assertEquals(
            Contact.objects.get(last_name="Norman").compare_with_another_contact(
                Contact.objects.get(last_name="Norman")
            ),
            1,
        )

    def test_detect_duplicate_different_contacts(self):
        self.assertTrue(
            Contact.objects.get(last_name="Norman").compare_with_another_contact(
                Contact.objects.get(last_name="Normna")
            )
            > 0
        )

        self.assertTrue(
            Contact.objects.get(last_name="Norman").compare_with_another_contact(
                Contact.objects.get(last_name="Normna")
            )
            < 1
        )

    def test_use_address_from_organization(self):
        self.assertFalse(self.contact.use_address_from_organization())

    def test_csv_output(self):
        self.assertIn("first_name", self.contact.get_header_as_csv_data())
        self.assertIn("Norman", self.contact.get_as_csv_data())


class OrganizationTestCase(TestCase):
    def setUp(self):
        self.org1 = OrganizationFactory()
        self.org2 = OrganizationFactory()

        for c in range(10):
            fc = ContactFactory()
            fc.save()
            moo = MemberOfOrganization()
            moo.contact = fc
            moo.organization = self.org1
            moo.use_address_from_organization = True
            moo.owning_group = GroupFactory()
            moo.save()
        return

    def test_count_contacts_in_organization(self):
        self.assertEquals(len(self.org1.get_contacts()), 10)
        self.assertEquals(len(self.org2.get_contacts()), 0)

    def test_find_duplicates(self):
        fc = ContactFactory()
        fc2 = ContactFactory(first_name=fc.first_name[:-1], last_name=fc.last_name[1:])
        similar = find_duplicated_contacts()

        self.assertEquals(len(similar), 1)
        for k in similar:
            self.assertIn(fc2, similar[k])
            self.assertIn(fc, similar[k])

    def test_get_address_from_organization(self):
        members = self.org1.get_contacts()
        c = members[0]
        addr = c.get_address()
        self.assertTrue(c.use_address_from_organization(self.org1))

        for a in LIST_ADDRESS_ATTR:
            if a not in ["phone", "fax"]:
                self.assertEquals(addr[a], getattr(self.org1, a))
            else:
                self.assertEquals(addr[a], getattr(c, a))
        fc = ContactFactory()
        fc.save()
        self.assertFalse(fc.use_address_from_organization(self.org1))

    def test_get_address_from_contact(self):
        fc = ContactFactory()
        fc.save()

        moo = MemberOfOrganization()
        moo.contact = fc
        moo.organization = self.org1
        moo.use_address_from_organization = False
        moo.owning_group = GroupFactory()
        moo.save()

        addr = fc.get_address()

        for a in LIST_ADDRESS_ATTR:
            self.assertNotEquals(addr[a], getattr(self.org1, a))
            self.assertEquals(addr[a], getattr(fc, a))

    def test_multiple_address_to_return(self):
        members = MemberOfOrganization.objects.filter(organization__pk=self.org1.pk)
        c = members[0].contact
        moo = MemberOfOrganization()
        moo.contact = c
        moo.organization = self.org2
        moo.use_address_from_organization = True
        moo.owning_group = GroupFactory()
        moo.save()

        with self.assertRaises(ValueError):
            addr = c.get_address()

        addr = c.get_address(for_organization=self.org1)

        for a in LIST_ADDRESS_ATTR:
            if a not in ["phone", "fax"]:
                self.assertEquals(addr[a], getattr(self.org1, a))
            else:
                self.assertEquals(addr[a], getattr(c, a))


class RelationBetweenOrganizationTestCase(TestCase):
    def test_str(self):
        group = GroupFactory()
        orga1 = OrganizationFactory(name="Orga1")
        orga2 = OrganizationFactory(name="Orga2")
        relation = RelationBetweenOrganization.objects.create(
            relation_name="la maison mère",
            first_organization=orga1,
            second_organization=orga2,
            owning_group=group,
        )
        self.assertEquals(str(relation), "Orga1 est la maison mère de Orga2")


class FolderModelTestCase(InitFapModelMixin, TestCase):
    def setUp(self):
        super().setUp()
        bad_file = File(open(join(FILES_DIR, "test.txt"), "rb"))
        good_file = File(open(join(FILES_DIR, "test.svg"), "rb"))
        self.upload_bad_file = SimpleUploadedFile(
            "test.txt", bad_file.read(), content_type="multipart/form-data"
        )
        self.upload_good_file = SimpleUploadedFile(
            "test.svg", good_file.read(), content_type="multipart/form-data"
        )

    def test_validate(self):
        bad_response = self.admin_client.post(
            reverse("admin:fac_foldermodel_add"),
            data={
                "name": "Testimo",
                "project": self.project.pk,
                "icon": "",
                "icon_marker": self.upload_bad_file.file,
                "link_to_contact": "true",
                "link_to_organization": "true",
                "statuses-TOTAL_FORMS": 0,
                "statuses-INITIAL_FORMS": 0,
                "statuses-MIN_NUM_FORMS": 0,
                "statuses-MAX_NUM_FORMS": 1000,
                "statuses-__prefix__-name": "",
                "statuses-__prefix__-order": 0,
                "statuses-__prefix__-color": "",
                "statuses-__prefix__-id": "",
                "statuses-__prefix__-folder_model": "",
                "categories-TOTAL_FORMS": 0,
                "categories-INITIAL_FORMS": 0,
                "categories-MIN_NUM_FORMS": 0,
                "categories-MAX_NUM_FORMS": 1000,
                "categories-__prefix__-name": "",
                "categories-__prefix__-order": 0,
                "categories-__prefix__-id": "",
                "categories-__prefix__-folder_model": "",
                "categories-empty-action_models-TOTAL_FORMS": 0,
                "categories-empty-action_models-INITIAL_FORMS": 0,
                "categories-empty-action_models-MIN_NUM_FORMS": 0,
                "categories-empty-action_models-MAX_NUM_FORMS": 1000,
                "categories-empty-action_models-__prefix__-name": "",
                "categories-empty-action_models-__prefix__-description": "",
                "categories-empty-action_models-__prefix__-trigger_status": "",
                "categories-empty-action_models-__prefix__-order": 0,
                "categories-empty-action_models-__prefix__-id": "",
                "categories-empty-action_models-__prefix__-category_model": "",
            },
        )
        assert bad_response.status_code == 200
        assert (
            bad_response.context_data["errors"][1][0] == "Le fichier n'est pas un SVG."
        )

        good_response = self.admin_client.post(
            reverse("admin:fac_foldermodel_add"),
            data={
                "name": "Testimo",
                "project": self.project.pk,
                "icon": "file-alt",
                "icon_marker": self.upload_good_file.file,
                "link_to_contact": "true",
                "link_to_organization": "true",
                "statuses-TOTAL_FORMS": 0,
                "statuses-INITIAL_FORMS": 0,
                "statuses-MIN_NUM_FORMS": 0,
                "statuses-MAX_NUM_FORMS": 1000,
                "statuses-__prefix__-name": "",
                "statuses-__prefix__-order": 0,
                "statuses-__prefix__-color": "",
                "statuses-__prefix__-id": "",
                "statuses-__prefix__-folder_model": "",
                "categories-TOTAL_FORMS": 0,
                "categories-INITIAL_FORMS": 0,
                "categories-MIN_NUM_FORMS": 0,
                "categories-MAX_NUM_FORMS": 1000,
                "categories-__prefix__-name": "",
                "categories-__prefix__-order": 0,
                "categories-__prefix__-id": "",
                "categories-__prefix__-folder_model": "",
                "categories-empty-action_models-TOTAL_FORMS": 0,
                "categories-empty-action_models-INITIAL_FORMS": 0,
                "categories-empty-action_models-MIN_NUM_FORMS": 0,
                "categories-empty-action_models-MAX_NUM_FORMS": 1000,
                "categories-empty-action_models-__prefix__-name": "",
                "categories-empty-action_models-__prefix__-description": "",
                "categories-empty-action_models-__prefix__-trigger_status": "",
                "categories-empty-action_models-__prefix__-order": 0,
                "categories-empty-action_models-__prefix__-id": "",
                "categories-empty-action_models-__prefix__-category_model": "",
            },
        )
        assert good_response.status_code == 302
        self.new_folder_model = FolderModel.objects.last()

    def extract_content_icon(self):
        assert self.new_folder_model.icon_marker_content == (
            '<path d="M60 58.064c8.185 0 14.819-6.633 14.819-14.819 0-8.185-6.'
            "634-14.819-14.819-14.819s-14.819 6.634-14.819 14.82c0 8.185 6.634"
            " 14.818 14.819 14.818zm10.373 7.192H68.44A20.176 20.176 0 0 1 60 "
            "67.108c-3.01 0-5.858-.671-8.44-1.852h-1.933c-8.59 0-15.56 "
            "3.483-15.56 12.073v4.816a5.559 5.559 0 0 0 5.557"
            " 5.558h40.752a5.559 5.559 0 0 0 "
            '5.557-5.558V77.33c0-8.59-6.97-12.073-15.56-12.073z" '
            'fill="none" stroke="#000" stroke-width="4.869"/>'
        )
