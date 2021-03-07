# -*- coding: utf-8 -*-
import datetime
import logging

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.template.loader import get_template

from accounts.models import User

from fac.models import Reminder

logger = logging.getLogger(__name__)  # NOQA


def get_reminders_and_send_email_for_user(user):
    count = 0
    # Retrieve contentType for contact and organization
    contact_type = ContentType.objects.get(app_label="fac", model="contact")
    organization_type = ContentType.objects.get(app_label="fac", model="organization")

    contact_reminders = (
        Reminder.objects.callout()
        .filter(
            (Q(owning_group__profile__in=[user]) & Q(persons=None))
            | Q(persons__in=[user]),
            date__lte=datetime.datetime.now(),
            content_type_contactable=contact_type,
        )
        .distinct()
    )
    organization_reminders = (
        Reminder.objects.callout()
        .filter(
            (Q(owning_group__profile__in=[user]) & Q(persons=None))
            | Q(persons__in=[user]),
            date__lte=datetime.datetime.now(),
            content_type_contactable=organization_type,
        )
        .distinct()
    )

    if contact_reminders.exists() or organization_reminders.exists():
        count = contact_reminders.count() + organization_reminders.count()
        context = {
            "user": user,
            "count": count,
            "contact_reminders": contact_reminders,
            "organization_reminders": organization_reminders,
        }

        html_message_template = get_template(
            "reminder/reminder_email.html"
        ).template.source

        user.send_email(
            subject="[FAC] {{count}} rappel{{ count|pluralize }} en attente",
            html_message=html_message_template,
            context=context,
        )
    return count


class Command(BaseCommand):
    """
    Sends the reminders for the FAC application
    Locally you can run it like this:
        $ inv django.run -c "SendReminders"

    It can be ran in a crontab like this (every day at 04:05 AM):
    5 4 * * * python manage.py SendReminders >> /tmp/send_reminders_logs 2>&1

    In production, it may looks like this:
    5 4 * * * inv exec -s fr.gederra.dialogwatt.dev -c django -a "python manage.py SendReminders" >> /tmp/send_reminders_logs 2>&1  # noqa
    """

    help = "Send reminders for contacts and organizations."  # NOQA: A003

    def handle(self, *args, **options):

        print("----------------------------------")
        print(self.help)
        print("----------------------------------")

        for user in (
            User.advisors.get_queryset().filter(is_active=True).order_by("group__name")
        ):
            try:
                count = get_reminders_and_send_email_for_user(user)
            except Exception as e:
                import sentry_sdk

                logger.error(f"SendReminders {e}")
                sentry_sdk.capture_exception(e)
            else:
                if count > 0:
                    print(f" - {user.email} ({count})")

        return
