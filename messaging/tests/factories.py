# -*- coding: utf-8 -*-

import factory
import factory.fuzzy

import faker

from accounts.tests.factories import GroupFactory

from messaging.models import SmsAccount, SmtpAccount

fake = faker.Factory.create("fr_FR")


class SmsAccountFactory(factory.django.DjangoModelFactory):
    """
    Generic factory for SmsAccount
    """

    class Meta:
        model = "messaging.SmsAccount"

    is_active = factory.lazy_attribute(lambda o: True)
    group = factory.SubFactory(GroupFactory)

    account_type = factory.fuzzy.FuzzyChoice(
        choices=[x[0] for x in SmsAccount.ACCOUNT_TYPES]
    )

    twilio_account = factory.lazy_attribute(lambda o: fake.uuid4())
    twilio_token = factory.lazy_attribute(lambda o: fake.uuid4())

    ovh_account = factory.lazy_attribute(lambda o: fake.uuid4())
    ovh_login = factory.fuzzy.FuzzyText(length=12)
    ovh_password = factory.fuzzy.FuzzyText(length=12)

    phone = factory.lazy_attribute(lambda o: fake.phone_number())
    monthly_limit = factory.fuzzy.FuzzyInteger(100, 100000)


class SmsAccountAsOvhFactory(SmsAccountFactory):
    """
    Factory for SmsAccount using OVH service
    """

    account_type = factory.lazy_attribute(lambda o: "ovh")


class SmsAccountAsTwilioFactory(SmsAccountFactory):
    """
    Factory for SmsAccount using Twilio service
    """

    account_type = factory.lazy_attribute(lambda o: "twilio")


class SmtpAccountFactory(factory.django.DjangoModelFactory):
    """
    Generic factory for SmtpAccount
    """

    class Meta:
        model = "messaging.SmtpAccount"

    is_active = factory.lazy_attribute(lambda o: True)
    group = factory.SubFactory(GroupFactory)
    from_username = factory.fuzzy.FuzzyText(length=20)
    smtp_type = factory.fuzzy.FuzzyChoice(
        choices=[x[0] for x in SmtpAccount.SMTP_TYPES]
    )
    mailgun_apikey = factory.lazy_attribute(lambda o: fake.uuid4())
    mailgun_monthly_limit = factory.fuzzy.FuzzyInteger(100, 100000)
    email_host = factory.lazy_attribute(lambda o: fake.hostname())
    email_port = factory.fuzzy.FuzzyInteger(25, 30)
    email_host_user = factory.fuzzy.FuzzyText(length=12)
    email_host_password = factory.fuzzy.FuzzyText(length=12)
    email_use_tls = factory.lazy_attribute(lambda o: False)
    email_use_ssl = factory.lazy_attribute(lambda o: False)


class SmtpAccountAsSmtpFactory(SmtpAccountFactory):
    """
    Factory for SmtpAccount using SMTP service
    """

    smtp_type = factory.lazy_attribute(lambda o: "smtp")


class SmtpAccountAsMailgunFactory(SmtpAccountFactory):
    """
    Factory for SmtpAccount using Mailgun service
    """

    smtp_type = factory.lazy_attribute(lambda o: "mailgun")
