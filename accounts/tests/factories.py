# -*- coding: utf-8 -*-

from factory import (
    PostGenerationMethodCall,
    SubFactory,
    lazy_attribute,
    post_generation,
)
from factory.django import DjangoModelFactory

import faker


fake = faker.Factory.create("fr_FR")


class UserFactory(DjangoModelFactory):
    class Meta:
        model = "accounts.User"

    first_name = lazy_attribute(lambda o: fake.first_name())
    last_name = lazy_attribute(lambda o: fake.last_name())
    password = PostGenerationMethodCall("set_password", "password")
    email = lazy_attribute(
        lambda o: f"{o.first_name}.{o.last_name}@{fake.domain_name()}".lower()
        .replace(" ", "-")
        .encode("ascii", "ignore")
        .decode("ascii")
    )


class GroupFactory(DjangoModelFactory):
    """
    Factory for Group. Usage : GroupFactory(territories=[commune1, commune2])
    """

    class Meta:
        model = "accounts.Group"

    name = lazy_attribute(lambda o: fake.name())
    is_admin = False
    admin_group = None
    email = lazy_attribute(
        lambda o: f"{fake.first_name()}.{fake.last_name()}@{fake.domain_name()}".lower()
        .replace(" ", "-")
        .encode("ascii", "ignore")
        .decode("ascii")
    )

    @post_generation
    def territories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for territory in extracted:
                self.territories.add(territory)


class AdminGroupFactory(GroupFactory):
    class Meta:
        model = "accounts.Group"

    name = lazy_attribute(lambda o: fake.name())
    is_admin = True
    admin_group = None


class ClientProfileFactory(UserFactory):
    """
    Factory for creating Client Profile
    """

    user_type = "client"
    phone = lazy_attribute(lambda o: fake.phone_number())


class AdvisorProfileFactory(UserFactory):
    """
    Factory for creating Advisor Profile
    """

    user_type = "advisor"
    phone = lazy_attribute(lambda o: fake.phone_number())
    group = SubFactory(GroupFactory)


class SuperAdvisorProfileFactory(UserFactory):
    """
    Factory for creating Advisor Profile
    """

    user_type = "superadvisor"
    phone = lazy_attribute(lambda o: fake.phone_number())
    group = SubFactory(GroupFactory)


class ManagerProfileFactory(UserFactory):
    """
    Factory for creating Manager Profile
    """

    user_type = "manager"
    phone = lazy_attribute(lambda o: fake.phone_number())
    group = SubFactory(GroupFactory)


class AdministratorProfileFactory(UserFactory):
    """
    Factory for creating Administrator Profile
    """

    user_type = "administrator"
    phone = lazy_attribute(lambda o: fake.phone_number())
    group = SubFactory(GroupFactory)


class RgpdConsentFactory(DjangoModelFactory):
    """
    Factory for creating RgpdConsent
    """

    class Meta:
        model = "accounts.RgpdConsent"

    user = SubFactory(UserFactory)
    allow_to_keep_data = fake.boolean()
    allow_to_use_email_to_send_reminder = fake.boolean()
    allow_to_use_phone_number_to_send_reminder = fake.boolean()
    allow_to_share_my_information_with_my_advisor = fake.boolean()
    allow_to_share_my_information_with_partners = fake.boolean()
