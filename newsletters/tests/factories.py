# -*- coding: utf-8 -*-
from django.utils.timezone import make_aware

import factory
import factory.fuzzy

import faker

from accounts.tests.factories import GroupFactory


fake = faker.Factory.create("fr_FR")


class NewslettersFactory(factory.django.DjangoModelFactory):
    pass


class GroupOfNewslettersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "newsletters.GroupOfNewsletters"

    group = factory.SubFactory(GroupFactory)
    slug = factory.lazy_attribute(lambda o: fake.slug())
    title = factory.lazy_attribute(lambda o: fake.text()[:100])
    is_active = factory.lazy_attribute(lambda o: fake.boolean())
    is_public = factory.lazy_attribute(lambda o: fake.boolean())
    header = None
    header_link = None
    footer = None
    footer_link = None
    description = factory.lazy_attribute(lambda o: fake.text())
    graphic_charter = "{}"


class NewsletterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "newsletters.Newsletter"

    group_of_newsletters = factory.SubFactory(GroupOfNewslettersFactory)
    slug = factory.lazy_attribute(lambda o: fake.slug())
    title = factory.lazy_attribute(lambda o: fake.text()[:100])
    is_active = factory.lazy_attribute(lambda o: fake.boolean())
    is_public = factory.lazy_attribute(lambda o: fake.boolean())
    publication_start_date = factory.lazy_attribute(
        lambda o: make_aware(fake.date_time(), is_dst=False)
    )
    publication_end_date = factory.lazy_attribute(
        lambda o: make_aware(fake.date_time(), is_dst=False)
    )
    description = factory.lazy_attribute(lambda o: fake.text())
    graphic_charter = "{}"
    plugins = "{}"
