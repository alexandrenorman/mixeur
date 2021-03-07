# -*- coding: utf-8 -*-

# https://django-test-plus.readthedocs.io/en/latest/
from test_plus.test import TestCase

from accounts.tests.factories import GroupFactory
from messaging.tests.factories import (
    SmtpAccountAsSmtpFactory,
    SmtpAccountAsMailgunFactory,
)

from messaging.helpers import get_smtp_connection


class GetSmtpConnectionTestCase(TestCase):
    def setUp(self):
        self.group = GroupFactory()
        return

    def test_smtp_connection_with_mailgun(self):
        smtp_account_for_advisor = SmtpAccountAsMailgunFactory(group=self.group)
        connection = get_smtp_connection(smtp_account_for_advisor)

        self.assertEquals(connection.__class__.__name__, "EmailBackend")
        self.assertEquals(connection.__class__.__module__, "anymail.backends.mailgun")
        self.assertEquals(connection.api_key, smtp_account_for_advisor.mailgun_apikey)

    def test_smtp_connection_with_smtp(self):
        smtp_account_for_advisor = SmtpAccountAsSmtpFactory(group=self.group)
        connection = get_smtp_connection(smtp_account_for_advisor)

        self.assertEquals(connection.__class__.__name__, "EmailBackend")
        self.assertEquals(
            connection.__class__.__module__, "django.core.mail.backends.smtp"
        )
        self.assertEquals(connection.host, smtp_account_for_advisor.email_host)
