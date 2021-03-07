from django.test import TestCase

from accounts.tests import GroupFactory
from fac.models import Budget
from fac.serializers import (
    ContactCSVSerializer,
    FolderSerializer,
    OrganizationCSVSerializer,
    TypeValorizationSerializer,
    FolderModelSerializer,
    ProjectSerializer,
)
from fac.tests.factories import (
    ContactFactory,
    FolderFactory,
    FolderModelFactory,
    OrganizationFactory,
    TypeValorizationFactory,
    CategoryModelFactory,
    ProjectFactory,
)
from .test_fap import InitFapModelMixin


class OrganizationCSVSerializerTestCase(TestCase):
    def test_csv(self):
        organizations = [OrganizationFactory() for _ in range(10)]
        serializer = OrganizationCSVSerializer(organizations)
        self.assertTrue("csv" in serializer.data)
        header, organizations_lines = serializer.data["csv"].strip().split("\r\n", 1)
        organizations_lines = organizations_lines.split("\r\n")
        self.assertEqual(len(organizations_lines), 10)


class ContactCSVSerializerTestCase(TestCase):
    def test_csv(self):
        contacts = [ContactFactory() for _ in range(10)]
        serializer = ContactCSVSerializer(contacts)
        self.assertTrue("csv" in serializer.data)
        header, contacts_lines = serializer.data["csv"].strip().split("\r\n", 1)
        contacts_lines = contacts_lines.split("\r\n")
        self.assertEqual(len(contacts_lines), 10)


class TypeValorizationSerializerTestCase(TestCase):
    def test_serialize(self):
        groups = [GroupFactory() for _ in range(10)]
        type_valorization = TypeValorizationFactory(groups=groups)
        serializer = TypeValorizationSerializer(type_valorization)
        self.assertEquals(
            {group.pk for group in groups}, set(serializer.data["groups"])
        )


class FolderSerializerTestCase(InitFapModelMixin, TestCase):
    def test_serialize(self):
        contact = ContactFactory()
        folder = FolderFactory(
            model=self.folder_model, owning_group=self.user_group, linked_object=contact
        )
        serialized = FolderSerializer(folder).data
        self.assertEquals(self.folder_model.pk, serialized["model"]["pk"])
        self.assertEquals(self.user_group.pk, serialized["owning_group"])
        self.assertEquals(self.type_valorization_1.pk, serialized["type_valorization"])


class FolderModelSerializerTestCase(TestCase):
    def test_serialize(self):
        categories = [CategoryModelFactory() for _ in range(10)]
        folder_model = FolderModelFactory(categories=categories)
        serialized = FolderModelSerializer(folder_model).data
        self.assertEquals(
            {category.pk for category in categories},
            {category["pk"] for category in serialized["categories"]},
        )


class ProjectSerializerTestCase(TestCase):
    def test_serialize_folder_models(self):
        type_valorizations = [TypeValorizationFactory() for _ in range(10)]
        groups = [GroupFactory() for _ in range(10)]
        project = ProjectFactory(type_valorizations=type_valorizations, groups=groups)
        folder_model = FolderModelFactory(icon="euro-sign", project=project)
        FolderFactory(model=folder_model)
        project.user_budgets = Budget.objects.none()
        serialized = ProjectSerializer(project).data
        self.assertEquals(folder_model.icon, serialized["folder_models"][0]["icon"])
