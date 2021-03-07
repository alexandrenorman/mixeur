# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site

from fac.models import Contact


class FacContactForDialogwatt(Contact):
    """
    Add properties to mimick a real User for being able to send email or SMS
    """

    class Meta:
        proxy = True

    @property
    def group(self):
        """
        No group
        """
        return None

    @property
    def allow_to_use_phone_number_to_send_reminder(self):
        """
        For dialogwatt / exchanges
        """
        if self.mobile_phone:
            return True

        return False

    @property
    def allow_to_use_email_to_send_reminder(self):
        """
        For dialogwatt / exchanges
        """
        if self.email:
            return True

        return False

    @property
    def preferred_white_labelling(self):
        """
        For dialogwatt / messaging
        """
        return self.owning_group.preferred_white_labelling

    def get_short_name(self):
        return self.email

    @property
    def short_name(self):
        return f"{self.email}"

    @property
    def display_name(self):
        """
        Return full_name
        """
        return self.full_name

    @property
    def is_administrator(self):
        return False

    @property
    def is_manager(self):
        return False

    @property
    def is_advisor(self):
        return False

    @property
    def is_superadvisor(self):
        return False

    @property
    def is_expert(self):
        return False

    @property
    def is_client(self):
        return True

    @property
    def is_contact(self):
        """
        False
        """
        return True

    @property
    def is_user(self):
        return False

    @property
    def is_admin(self):
        return False

    @property
    def full_name(self):
        """
        Return display name as 'first_name last_name'
        """
        if self.first_name:
            return f"{self.first_name} {self.last_name}"
        return f"{self.last_name}"

    def send_email(  # NOQA: CFQ002
        self,
        subject: str,
        html_message: str = None,
        context: dict = None,
        sender=None,
        as_background_task=True,
        use_fallback: bool = True,
    ):
        """
        Sends an email to this User.

        :subject: mail subject
        :html_message: mail content as html text
        :context: context for template generation
        :sender: sender of the message
        :as_background_task: send using task
        """
        from messaging.helpers import EmailToUserHelper

        context = context if context else {}

        email_to_user_helper = EmailToUserHelper(account=self)
        task = email_to_user_helper.send_email(
            subject=subject,
            message=html_message,
            context=context,
            sender=sender,
            as_background_task=as_background_task,
            use_fallback=use_fallback,
        )

        return task

    def send_sms(
        self, message: str, context: dict = None, sender=None, as_background_task=True
    ):
        """
        Sends an sms to this User.

        :message: sms content as ascii text
        :context: context for template generation
        :sender: sender of the message
        :as_background_task: send using task
        """
        from messaging.helpers import SmsToUserHelper

        context = context if context else {}

        sms_to_user_helper = SmsToUserHelper(account=self)
        task = sms_to_user_helper.send_sms(
            message=message,
            context=context,
            sender=sender,
            as_background_task=as_background_task,
        )

        return task

    def user_site(self):
        if self.preferred_white_labelling:
            return self.preferred_white_labelling

        return Site.objects.get_current()

    @property
    def can_login(self) -> bool:
        return False

    @property
    def allowed_methods_for_contact(self):
        """
        Return allowed methods for contacting this contact
        """
        methods = []

        if self.allow_to_use_phone_number_to_send_reminder:
            methods.append("sms")

        if self.allow_to_use_email_to_send_reminder:
            methods.append("mail")

        return methods
