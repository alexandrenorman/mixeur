from django.apps import AppConfig
from django.db.utils import ProgrammingError

from config import settings

from core.helpers import is_jenkins_build


class MessagingAppConfig(AppConfig):
    name = "messaging"

    def ready(self):
        if settings.OVERRIDE_SMTP_AND_SMS and not is_jenkins_build():
            print("\n----------------------------------")
            print("MessagingConfig (OVERRIDE_SMTP_AND_SMS)")
            print("----------------------------------")
            try:
                self.set_smtp_config_for_mixeur_local()
                self.set_sms_config_for_mixeur_local()
            except ProgrammingError:
                print("Nothin done")

            print("----------------------------------")

    def set_smtp_config_for_mixeur_local(self):
        print("* OVERRIDE SMTP config")
        from messaging.models import SmtpAccount
        from accounts.models import Group

        for group in Group.objects.all():
            obj, created = SmtpAccount.objects.get_or_create(
                group=group,
                defaults={
                    "is_active": True,
                    "name": f"SMTP debug conf for {group.name}",
                    "from_username": f"mixeur debug mail for {group.name}",
                    "smtp_type": "smtp",
                    "email_host": "mail",
                    "email_port": 1025,
                    "email_host_user": "anonymous",
                    "email_host_password": "password",
                    "email_use_tls": False,
                    "email_use_ssl": False,
                },
            )
            obj.is_active = True
            obj.name = f"SMTP debug conf for {group.name}"
            obj.from_username = f"mixeur debug mail for {group.name}"
            obj.smtp_type = "smtp"
            obj.email_host = "mail"
            obj.email_port = 1025
            obj.email_host_user = "anonymous"
            obj.email_host_password = "password"
            obj.email_use_tls = False
            obj.email_use_ssl = False

            obj.save()

    def set_sms_config_for_mixeur_local(self):
        print("* OVERRIDE SMS config")
        from messaging.models import SmsAccount
        from accounts.models import Group

        for group in Group.objects.all():
            obj, created = SmsAccount.objects.get_or_create(
                group=group,
                defaults={
                    "account_type": "mail",
                },  # NOQA: E231
            )
            obj.account_type = "mail"
            obj.is_active = True

            obj.save()
