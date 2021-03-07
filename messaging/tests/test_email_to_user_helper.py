# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

# https://django-test-plus.readthedocs.io/en/latest/
from test_plus.test import TestCase

from accounts.tests.factories import (
    AdvisorProfileFactory,
    ClientProfileFactory,
    GroupFactory,
)

from messaging.helpers import EmailToUserHelper
from messaging.tests.factories import SmtpAccountAsSmtpFactory


from white_labelling.models import WhiteLabelling


class EmailToUserHelperTestCase(TestCase):
    def setUp(self):
        self.group = GroupFactory()
        self.advisor = AdvisorProfileFactory(group=self.group)
        self.client = ClientProfileFactory()

        self.smtp_account_for_advisor = SmtpAccountAsSmtpFactory(group=self.group)

        self.email_to_advisor = EmailToUserHelper(
            account=self.advisor, white_labelling=None
        )
        self.email_to_client = EmailToUserHelper(
            account=self.client, white_labelling=None
        )
        return

    def test_from_field(self):
        self.assertEquals(
            self.email_to_advisor._from_field,
            f"{self.smtp_account_for_advisor.from_username} <{self.smtp_account_for_advisor.email_host_user}>",
        )

    def test_from_name(self):
        self.assertEquals(
            self.email_to_advisor._from_name,
            self.smtp_account_for_advisor.from_username,
        )

    def test_from_email(self):
        self.assertEquals(
            self.email_to_advisor._from_email,
            self.smtp_account_for_advisor.email_host_user,
        )

    def test_stupid(self):
        from messaging.models import SmtpAccount

        self.assertTrue(self.advisor.is_expert)
        self.assertTrue(SmtpAccount.objects.filter(group=self.group).exists())
        self.assertTrue(SmtpAccount.objects.filter(group=self.advisor.group).exists())

    def test_get_smtp_account_for_advisor(self):
        self.assertEquals(
            self.email_to_advisor._get_smtp_account(), self.smtp_account_for_advisor
        )

    def test_get_smtp_account_for_client(self):
        self.assertEquals(self.email_to_client._get_smtp_account(), None)

    def test_get_smtp_account_with_specified_whitelabelling(self):
        smtp_account_for_specific_wl = SmtpAccountAsSmtpFactory(group=None)
        wl = WhiteLabelling.objects.create(
            domain="test-specific.hespul.org",
            smtp_account=smtp_account_for_specific_wl,
            is_default=False,
        )
        email_to_client = EmailToUserHelper(account=self.client, white_labelling=wl)
        self.assertEquals(
            email_to_client._get_smtp_account(), smtp_account_for_specific_wl
        )

    def test_get_smtp_account_with_default_whitelabelling(self):
        smtp_account_for_system_wide = SmtpAccountAsSmtpFactory(group=None)
        WhiteLabelling.objects.create(
            domain="test.hespul.org",
            smtp_account=smtp_account_for_system_wide,
            is_default=True,
        )
        email_to_client = EmailToUserHelper(account=self.client, white_labelling=None)
        self.assertEquals(
            email_to_client._get_smtp_account(), smtp_account_for_system_wide
        )

    def test_white_labelling_to_use_specified(self):
        smtp_account_for_specific_wl = SmtpAccountAsSmtpFactory(group=None)
        wl = WhiteLabelling.objects.create(
            domain="test-specific.hespul.org",
            smtp_account=smtp_account_for_specific_wl,
            is_default=False,
        )
        email_to_client = EmailToUserHelper(account=self.client, white_labelling=wl)

        self.assertEquals(email_to_client.white_labelling, wl)

        self.assertEquals(email_to_client._white_labelling_to_use(wl), wl)

    def test_white_labelling_from_group(self):
        smtp_account_for_specific_wl = SmtpAccountAsSmtpFactory(group=None)
        wl = WhiteLabelling.objects.create(
            domain="test-specific.hespul.org",
            smtp_account=smtp_account_for_specific_wl,
            is_default=False,
        )
        self.group.white_labelling = wl
        self.group.save()

        email_to_advisor = EmailToUserHelper(account=self.advisor, white_labelling=None)

        self.assertEquals(email_to_advisor._white_labelling_to_use(), wl)

    def test_white_labelling_from_default(self):
        smtp_account_for_specific_wl = SmtpAccountAsSmtpFactory(group=None)
        wl = WhiteLabelling.objects.create(
            domain="test-specific.hespul.org",
            smtp_account=smtp_account_for_specific_wl,
            is_default=True,
        )
        email_to_advisor = EmailToUserHelper(account=self.advisor, white_labelling=None)

        self.assertEquals(email_to_advisor._white_labelling_to_use(), wl)

    def test_white_labelling_is_none(self):
        email_to_advisor = EmailToUserHelper(account=self.advisor, white_labelling=None)

        self.assertTrue(email_to_advisor._white_labelling_to_use() is None)

    def test_template_path(self):
        self.assertEquals(
            self.email_to_advisor._template_path("file"),
            "/app/django/messaging/templates/messaging/file",
        )

    def test_format_subject(self):
        self.assertEquals(
            self.email_to_advisor._format_subject("subject\n"), "mixeur - subject"
        )

    def test_format_html_message(self):
        message = "Welcome {{name}}"
        self.email_to_advisor.context = {"name": "Alexandre"}
        self.assertEquals(
            self.email_to_advisor._format_html_message(message),
            self._rendered_html_message,
        )

    def test_background_send_email_to_user(self):
        self.email_to_advisor._background_send_email_to_user = MagicMock(
            name="background_send_email_to_user"
        )

        self.email_to_advisor.send_email(
            subject="subject", message="Welcome {{name}}", context={"name": "Alexandre"}
        )

        self.email_to_advisor._background_send_email_to_user.assert_called_once_with(
            smtp_account=self.smtp_account_for_advisor.pk,
            from_email=self.email_to_advisor._from_field,
            recipient_list=[self.advisor.email],
            subject="mixeur - subject",
            html_message=self._rendered_html_message,
            ascii_message=self._rendered_ascii_message,
            attachments=None,
        )

    @property
    def _rendered_html_message(self):
        return (
            "<html>\n\n  <head></head><body>\n    <!-- HEADER -->\n    "
            + '<div class="header">\n    </div>\n\nWelcome Alexandre\n\n    '
            + '<!-- FOOTER -->\n    <div class="footer">\n    </div>\n  </body>\n</html>'
        )

    @property
    def _rendered_ascii_message(self):
        return "Welcome Alexandre\n\n"
