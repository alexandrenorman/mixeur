# -*- coding: utf-8 -*-

import random

from django.utils.timezone import make_aware

import factory
import factory.fuzzy

import faker
from faker.providers import BaseProvider

from accounts.tests.factories import (
    AdvisorProfileFactory,
    ClientProfileFactory,
    GroupFactory,
)

from dialogwatt.models import Exchange, Notification

from fac.tests.factories import ContactFactory


fake = faker.Factory.create("fr_FR")


class ChoiceProvider(BaseProvider):
    def choice(self, source):
        return random.choice(source)[0]


# Add the TravelProvider to our faker object
fake.add_provider(ChoiceProvider)


class CatchmentAreaFactory(factory.django.DjangoModelFactory):
    """
    Factory for CatchmentArea. Usage : CatchmentAreaFactory()
    """

    class Meta:
        model = "dialogwatt.CatchmentArea"

    name = factory.lazy_attribute(lambda o: fake.name())

    group = factory.SubFactory(GroupFactory)
    description = factory.lazy_attribute(lambda o: fake.text())
    additionnal_information = factory.lazy_attribute(lambda o: fake.text())

    @factory.post_generation
    def territories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for territorie in extracted:
                self.territories.add(territorie)


class PlaceFactory(factory.django.DjangoModelFactory):
    """
    Factory for Place. Usage : PlaceFactory(groups=[g1, g2])
    """

    class Meta:
        model = "dialogwatt.Place"

    name = factory.lazy_attribute(lambda o: fake.name())
    slug = factory.lazy_attribute(lambda o: fake.slug())
    presentation = factory.lazy_attribute(lambda o: fake.text())
    phone = factory.lazy_attribute(lambda o: fake.phone_number())
    address = factory.lazy_attribute(lambda o: fake.address())
    url = factory.lazy_attribute(lambda o: fake.uri())
    email = factory.lazy_attribute(
        lambda o: f"{fake.first_name()}.{fake.last_name()}@{fake.domain_name()}".lower()
        .replace(" ", "-")
        .encode("ascii", "ignore")
        .decode("ascii")
    )

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)


class ReasonFactory(factory.django.DjangoModelFactory):
    """
    Factory for Reason. Usage : ReasonFactory(groups=[g1, g2])
    """

    class Meta:
        model = "dialogwatt.Reason"

    name = factory.lazy_attribute(lambda o: fake.name())
    is_active = factory.lazy_attribute(lambda o: fake.boolean())
    duration = factory.lazy_attribute(
        lambda o: fake.pydecimal(
            left_digits=2, right_digits=0, positive=True, min_value=0, max_value=99
        )
    )
    group = factory.SubFactory(GroupFactory)
    internal_description = factory.lazy_attribute(
        lambda o: fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)
    )
    show_description = factory.lazy_attribute(lambda o: fake.boolean())
    description = factory.lazy_attribute(
        lambda o: fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)
    )


class SlotFactory(factory.django.DjangoModelFactory):
    """
    Factory for Slot. Usage : SlotFactory()
    """

    class Meta:
        model = "dialogwatt.Slot"

    text = factory.lazy_attribute(lambda o: fake.name())
    group = factory.SubFactory(GroupFactory)

    status = factory.lazy_attribute(lambda o: "validated")

    description = factory.lazy_attribute(lambda o: fake.text())

    start_date = factory.lazy_attribute(
        lambda o: make_aware(fake.date_time(), is_dst=False)
    )
    end_date = factory.lazy_attribute(
        lambda o: make_aware(fake.date_time(), is_dst=False)
    )

    place = factory.SubFactory(PlaceFactory)
    catchment_area = factory.SubFactory(CatchmentAreaFactory)

    @factory.post_generation
    def reasons(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for reason in extracted:
                self.reasons.add(reason)

    @factory.post_generation
    def advisors(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for advisor in extracted:
                self.advisors.add(advisor)


class AppointmentFactory(factory.django.DjangoModelFactory):
    """
    Factory for Appointment. Usage : AppointmentFactory()
    """

    class Meta:
        model = "dialogwatt.Appointment"

    start_date = factory.lazy_attribute(
        lambda o: make_aware(fake.date_time(), is_dst=False)
    )
    end_date = factory.lazy_attribute(
        lambda o: make_aware(fake.date_time(), is_dst=False)
    )

    subject = factory.fuzzy.FuzzyText(length=25)
    advisor = factory.SubFactory(AdvisorProfileFactory)
    client_or_contact = factory.SubFactory(ClientProfileFactory)
    place = factory.SubFactory(PlaceFactory)
    slot = factory.SubFactory(SlotFactory)
    reason = factory.SubFactory(ReasonFactory)
    description = factory.lazy_attribute(lambda o: fake.text())
    has_been_honored = factory.lazy_attribute(lambda o: fake.boolean())


class NotificationFactory(factory.django.DjangoModelFactory):
    """
    Factory for Notifaction. Usage: AppointmentFactory()
    """

    class Meta:
        model = "dialogwatt.Notification"

    name = factory.lazy_attribute(lambda o: fake.name())
    group = factory.SubFactory(GroupFactory)
    is_active = factory.lazy_attribute(lambda o: fake.boolean())
    trigger = factory.lazy_attribute(lambda o: fake.choice(Notification.TRIGGER))
    term = factory.lazy_attribute(lambda o: fake.choice(Notification.TERM))
    term_days = factory.Maybe(
        factory.LazyAttribute(lambda o: o.term == "delayed"),
        yes_declaration=fake.pydecimal(
            left_digits=2, right_digits=0, positive=True, min_value=1, max_value=15
        ),
        no_declaration=0,
    )
    term_day_type = factory.lazy_attribute(
        lambda o: fake.choice(Notification.TERM_DAY_TYPE)
    )
    term_after_before = factory.lazy_attribute(
        lambda o: fake.choice(Notification.TERM_AFTER_BEFORE)
    )
    term_time = factory.lazy_attribute(lambda o: fake.time_object(end_datetime=None))
    all_reasons = factory.lazy_attribute(lambda o: fake.boolean())
    all_places = factory.lazy_attribute(lambda o: fake.boolean())
    to = factory.lazy_attribute(lambda o: fake.choice(Notification.TO))
    sms_is_active = factory.lazy_attribute(lambda o: fake.boolean())
    sms_message = factory.Maybe(
        "sms_is_active",
        yes_declaration=fake.sentence(
            nb_words=6, variable_nb_words=True, ext_word_list=None
        ),
        no_declaration="",
    )
    mail_is_active = factory.lazy_attribute(lambda o: fake.boolean())
    mail_subject = factory.Maybe(
        "mail_is_active",
        yes_declaration=fake.sentence(
            nb_words=6, variable_nb_words=True, ext_word_list=None
        ),
        no_declaration="",
    )
    mail_message = factory.Maybe(
        "mail_is_active",
        yes_declaration=fake.sentence(
            nb_words=6, variable_nb_words=True, ext_word_list=None
        ),
        no_declaration="",
    )
    chat_is_active = factory.lazy_attribute(lambda o: fake.boolean())
    chat_message = factory.Maybe(
        "chat_is_active",
        yes_declaration=fake.sentence(
            nb_words=6, variable_nb_words=True, ext_word_list=None
        ),
        no_declaration="",
    )

    @factory.post_generation
    def advisors(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for advisor in extracted:
                self.advisors.add(advisor)

    @factory.post_generation
    def places(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for place in extracted:
                self.places.add(place)

    @factory.post_generation
    def reasons(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for reason in extracted:
                self.reasons.add(reason)


class ExchangeFactory(factory.django.DjangoModelFactory):
    """
    Factory for Exchange
    """

    class Meta:
        model = "dialogwatt.Exchange"

    schedule = factory.lazy_attribute(
        lambda o: make_aware(fake.date_time(), is_dst=False)
    )
    background_task = None
    from_account = factory.SubFactory(AdvisorProfileFactory)
    to_account = factory.SubFactory(ClientProfileFactory)
    group = factory.SubFactory(GroupFactory)
    trigger = factory.fuzzy.FuzzyText(length=25)
    subject = factory.fuzzy.FuzzyText(length=25)
    message_sms = factory.fuzzy.FuzzyText(length=100)
    message_mail_ascii = factory.fuzzy.FuzzyText(length=250)
    message_mail_html = factory.fuzzy.FuzzyText(length=250)
    message_type = factory.fuzzy.FuzzyChoice(
        choices=[x[0] for x in Exchange.MESSAGE_TYPE]
    )
    has_been_sent_on = factory.lazy_attribute(
        lambda o: make_aware(fake.date_time(), is_dst=False)
    )
    has_been_received_on = factory.lazy_attribute(
        lambda o: make_aware(fake.date_time(), is_dst=False)
    )
    has_been_opened_on = factory.lazy_attribute(
        lambda o: make_aware(fake.date_time(), is_dst=False)
    )


class FacContactForDialogwattFactory(ContactFactory):
    class Meta:
        model = "dialogwatt.FacContactForDialogwatt"
