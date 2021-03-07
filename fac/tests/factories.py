from django.contrib.contenttypes.models import ContentType

import factory
from factory import SubFactory, lazy_attribute
from factory.django import DjangoModelFactory

import faker

from accounts.tests.factories import GroupFactory, UserFactory

faker = faker.Factory.create("fr_FR")


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = "fac.Contact"

    first_name = lazy_attribute(lambda o: faker.first_name())
    last_name = lazy_attribute(lambda o: faker.last_name())
    email = lazy_attribute(
        lambda o: f"{o.first_name}.{o.last_name}@example.com".lower().replace(" ", "-")
    )
    address = lazy_attribute(lambda o: faker.address())
    zipcode = lazy_attribute(lambda o: faker.postcode())
    town = lazy_attribute(lambda o: faker.city())
    country = lazy_attribute(lambda o: faker.country())
    phone = lazy_attribute(lambda o: faker.phone_number())
    mobile_phone = lazy_attribute(lambda o: faker.phone_number())
    fax = lazy_attribute(lambda o: faker.phone_number())
    owning_group = SubFactory(GroupFactory)
    client_account = SubFactory(UserFactory)


class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = "fac.Organization"

    name = lazy_attribute(lambda o: faker.name())
    address = lazy_attribute(lambda o: faker.address())
    zipcode = lazy_attribute(lambda o: faker.postcode())
    town = lazy_attribute(lambda o: faker.city())
    country = lazy_attribute(lambda o: faker.country())
    phone = lazy_attribute(lambda o: faker.phone_number())
    fax = lazy_attribute(lambda o: faker.phone_number())
    owning_group = SubFactory(GroupFactory)


class TagFactory(DjangoModelFactory):
    class Meta:
        model = "fac.Tag"

    name = lazy_attribute(lambda o: faker.name()[:100])
    description = lazy_attribute(lambda o: faker.text()[:100])
    owning_group = SubFactory(GroupFactory)


class RelationBetweenOrganizationFactory(DjangoModelFactory):
    class Meta:
        model = "fac.RelationBetweenOrganization"

    first_organization = SubFactory(OrganizationFactory)
    second_organization = SubFactory(OrganizationFactory)
    relation_name = lazy_attribute(lambda o: faker.name()[:100])
    owning_group = SubFactory(GroupFactory)


class NoteFactory(DjangoModelFactory):
    class Meta:
        model = "fac.Note"

    owning_group = SubFactory(GroupFactory)
    note = lazy_attribute(lambda o: faker.name()[:100])


class MemberOfOrganizationFactory(DjangoModelFactory):
    class Meta:
        model = "fac.MemberOfOrganization"

    owning_group = SubFactory(GroupFactory)
    contact = SubFactory(ContactFactory)
    organization = SubFactory(OrganizationFactory)
    title_in_organization = lazy_attribute(lambda o: faker.name()[:50])


class PeriodFactory(DjangoModelFactory):
    class Meta:
        model = "fac.Period"

    name = lazy_attribute(lambda o: faker.sentence())
    date_start = lazy_attribute(lambda o: faker.date_object())
    date_end = lazy_attribute(lambda o: faker.date_object())


class TypeValorizationFactory(DjangoModelFactory):
    class Meta:
        model = "fac.TypeValorization"

    name = lazy_attribute(lambda o: faker.city())

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)


class ValorizationFactory(DjangoModelFactory):
    class Meta:
        model = "fac.Valorization"

    act = lazy_attribute(lambda o: faker.boolean())
    amount = lazy_attribute(
        lambda o: faker.pydecimal(positive=True, left_digits=2, right_digits=2)
    )
    type_valorization = SubFactory(TypeValorizationFactory)
    period = SubFactory(PeriodFactory)


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = "fac.Project"

    name = lazy_attribute(lambda o: faker.sentence())

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)

    @factory.post_generation
    def type_valorizations(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for type_valorization in extracted:
                self.type_valorizations.add(type_valorization)


class BudgetFactory(DjangoModelFactory):
    class Meta:
        model = "fac.Budget"

    period = SubFactory(PeriodFactory)
    total_envelope = lazy_attribute(lambda o: faker.random_int(2000, 4000))
    group = SubFactory(GroupFactory)
    project = SubFactory(ProjectFactory)


class FolderModelFactory(DjangoModelFactory):
    class Meta:
        model = "fac.FolderModel"

    name = lazy_attribute(lambda o: faker.sentence())
    project = SubFactory(ProjectFactory)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.categories.add(category)


class StatusFactory(DjangoModelFactory):
    class Meta:
        model = "fac.Status"

    name = lazy_attribute(lambda o: faker.sentence())
    folder_model = SubFactory(FolderModelFactory)


class CategoryModelFactory(DjangoModelFactory):
    class Meta:
        model = "fac.CategoryModel"

    name = lazy_attribute(lambda o: faker.sentence())
    folder_model = SubFactory(FolderModelFactory)


class ActionModelFactory(DjangoModelFactory):
    class Meta:
        model = "fac.ActionModel"

    name = lazy_attribute(lambda o: faker.sentence())
    category_model = SubFactory(CategoryModelFactory)
    trigger_status = SubFactory(StatusFactory)
    order = lazy_attribute(lambda o: faker.random_int(0, 20))
    default = True

    @factory.post_generation
    def valorizations(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for valorization in extracted:
                self.valorizations.add(valorization)


class FolderFactory(DjangoModelFactory):
    class Meta:
        model = "fac.Folder"

    description = lazy_attribute(lambda o: faker.sentence())
    model = SubFactory(FolderModelFactory)
    owning_group = SubFactory(GroupFactory)
    type_valorization = SubFactory(TypeValorizationFactory)


class ActionFactory(DjangoModelFactory):
    class Meta:
        model = "fac.Action"

    duration = lazy_attribute(
        lambda o: faker.pydecimal(positive=True, left_digits=2, right_digits=2)
    )
    date = lazy_attribute(lambda o: faker.date_object())
    done = False
    message = lazy_attribute(lambda o: faker.sentence())
    folder = SubFactory(FolderFactory)
    model = SubFactory(ActionModelFactory)
    valorization = SubFactory(ValorizationFactory)


class ListFactory(DjangoModelFactory):
    class Meta:
        model = "fac.List"

    title = lazy_attribute(lambda o: faker.name())
    owning_group = SubFactory(GroupFactory)


class ObjectiveStatusFactory(DjangoModelFactory):
    class Meta:
        model = "fac.ObjectiveStatus"

    name = lazy_attribute(lambda o: faker.name())
    period = SubFactory(PeriodFactory)
    group = SubFactory(GroupFactory)
    status = SubFactory(StatusFactory)
    nb_statuses = 5


class ObjectiveActionFactory(DjangoModelFactory):
    class Meta:
        model = "fac.ObjectiveAction"

    name = lazy_attribute(lambda o: faker.name())
    period = SubFactory(PeriodFactory)
    group = SubFactory(GroupFactory)
    nb_actions = 5


class ReminderFactory(DjangoModelFactory):
    class Meta:
        exclude = ["linked_object_task"]
        abstract = True

    owning_group = SubFactory(GroupFactory)

    object_id_task = factory.SelfAttribute("linked_object_task.id")
    content_type_task = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.linked_object_task)
    )

    date = lazy_attribute(lambda o: faker.date())


class ReminderNoteFactory(ReminderFactory):
    linked_object_task = factory.SubFactory(NoteFactory)

    class Meta:
        model = "fac.Reminder"


class ReminderActionFactory(ReminderFactory):
    linked_object_task = factory.SubFactory(ActionFactory)

    class Meta:
        model = "fac.Reminder"


class FileActionFactory(DjangoModelFactory):
    class Meta:
        model = "fac.File"

    owning_group = SubFactory(GroupFactory)

    object_id = factory.SelfAttribute("linked_object.id")
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.linked_object)
    )
    linked_object = factory.SubFactory(ActionFactory)
    document = factory.django.FileField(filename="the_file.txt")
