# -*- coding: utf-8 -*-

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import models
from django.template import loader
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _


from phonenumber_field.modelfields import PhoneNumberField

from core.models import MixeurBaseModel

from messaging.helpers import EmailToUserHelper, SmsToUserHelper

from visit_report.models import Housing

from white_labelling.models import WhiteLabelling

from .rgpd_consent import RgpdConsent


class UserClientManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type="client")


class UserProfessionalManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type="professional")


class UserAdvisorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type__in=("advisor", "superadvisor"))


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        user = self.model(email=self.normalize_email(email), is_active=True, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_client(self, email, password, **kwargs):
        return self.create_user(email, password, user_type="client", **kwargs)

    def create_advisor(self, email, password, **kwargs):
        return self.create_user(email, password, user_type="advisor", **kwargs)

    def create_professional(self, email, password, **kwargs):
        return self.create_user(email, password, user_type="professional", **kwargs)

    def create_superadvisor(self, email, password, **kwargs):
        return self.create_user(email, password, user_type="superadvisor", **kwargs)

    def create_manager(self, email, password, **kwargs):
        return self.create_user(email, password, user_type="manager", **kwargs)

    def create_administrator(self, email, password, **kwargs):
        return self.create_user(email, password, user_type="administrator", **kwargs)

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=email, is_staff=True, is_superuser=True, is_active=True, **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


def profile_directory_path(instance, filename):
    return f"profiles/{instance.id}/{filename}"


class User(AbstractBaseUser, PermissionsMixin, MixeurBaseModel):
    USER_TYPES = (
        ("client", _("Client")),
        ("professional", _("Professionnel")),
        ("advisor", _("Conseiller")),
        ("superadvisor", _("Super conseiller")),
        ("manager", _("Responsable")),
        ("administrator", _("Administrateur")),
    )
    CIVILITIES = (("M.", _("M.")), ("Mme", _("Mme")), ("Mlle", _("Mlle")))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = _("Utilisateur")

    objects = UserManager()
    clients = UserClientManager()
    advisors = UserAdvisorManager()
    professionals = UserProfessionalManager()

    email = models.EmailField(unique=True)
    civility = models.CharField(
        max_length=8,
        choices=CIVILITIES,
        blank=True,
        verbose_name=_("civility"),
        default="",
    )
    first_name = models.CharField(
        _("first name"), max_length=300, blank=True, default=""
    )
    last_name = models.CharField(_("last name"), max_length=300)

    is_staff = models.BooleanField(
        _("staff status"), default=False, help_text=_("admin ?")
    )
    is_active = models.BooleanField(
        _("active"), default=True, help_text=_("Active user ?")
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    user_type = models.CharField(
        _("Profil d'utilisateur"), choices=USER_TYPES, default="client", max_length=20
    )

    title = models.CharField(
        _("Titre ou fonction"), blank=True, max_length=100, default=""
    )

    phone = PhoneNumberField(
        _("Numéro de téléphone"), max_length=100, blank=True, null=True
    )
    color = models.CharField(_("Color"), blank=False, max_length=10, default="#888888")

    phone_cache = models.CharField(
        _("Cache pour le numéro de téléphone"),
        blank=True,
        max_length=100,
        default="",
    )
    group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe"),
        help_text=_("Structure d'appartenance"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="profile",
    )

    white_labelling = models.ForeignKey(
        "white_labelling.WhiteLabelling",
        verbose_name=_("Domaine / marque blanche"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="profile",
    )
    profile_pic = models.ImageField(
        upload_to=profile_directory_path,
        blank=True,
        default="",
    )

    appointments = GenericRelation(
        "dialogwatt.Appointment",
        related_query_name="user",
        content_type_field="content_type",
        object_id_field="object_id",
    )

    def clean(self):
        self.email = self.email.lower()
        if (
            self.user_type == "client" or self.user_type == "professional"
        ) and self.is_superuser:
            raise ValidationError(
                _(
                    "Un profil « client » ou « professionnel » ne peut pas être superuser."
                )
            )
        if self.is_client and self.group:
            raise ValidationError(
                _(
                    "Un profil « client » ou « professionnel » ne peut pas être affecté à un groupe."
                )
            )
        if self.is_superuser and (
            self.is_manager or self.is_advisor or self.is_client or self.is_professional
        ):
            raise ValidationError(
                _(
                    "Un utilisateur SuperUser ne peut pas être Manager, Professionnel, Conseiller or Client."
                )
            )
        if self.is_administrator and self.group:
            raise ValidationError(
                _("Un profil « administrateur » ne peut pas être affecté à un groupe.")
            )
        if self.is_manager and not self.group:
            raise ValidationError(
                _("Un profil « manager » doit appartenir à un groupe admin.")
            )
        if self.is_manager and not self.group.is_admin:
            raise ValidationError(
                _(
                    "Un profil « manager » ne peut pas être appartenir à un groupe normal."
                )
            )
        if self.is_advisor and not self.group:
            raise ValidationError(
                _("Un profil « conseiller » doit être affecté à un groupe.")
            )
        if self.is_professional and not self.group:
            raise ValidationError(
                _("Un profil « professionnel » doit être affecté à un groupe.")
            )
        if self.is_advisor and self.group and self.group.is_admin:
            raise ValidationError(
                _(
                    "Un profil « conseiller » ne peut pas être affecté à un groupe d'administration."
                )
            )

    def save(self, *args, **kwargs):
        if self.phone:
            self.phone_cache = f"0{self.phone.national_number}"

        super().save(*args, **kwargs)

    def get_short_name(self):
        return self.email

    @property
    def preferred_white_labelling(self):
        if self.is_expert and self.group:
            return self.group.preferred_white_labelling

        if self.white_labelling:
            return self.white_labelling

        default = WhiteLabelling.objects.filter(is_active=True, is_default=True)
        if default.exists():
            return default.first()

        return None

    @property
    def address(self):
        return ""

    @property
    def mobile_phone(self):
        return self.phone

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
        """
        True if user_type is "administrator" or user is superuser
        """
        return self.user_type == "administrator" or self.is_superuser

    @property
    def is_manager(self):
        """
        True if user_type is "manager" and user is not superuser
        """
        return self.user_type == "manager" and not self.is_superuser

    @property
    def is_advisor(self):
        """
        True if (user_type is "advisor" or "superadvisor") and user is not superuser
        """
        return (
            self.user_type == "advisor" or self.user_type == "superadvisor"
        ) and not self.is_superuser

    @property
    def is_superadvisor(self):
        """
        True if user_type is "superadvisor" and user is not superuser
        """
        return self.user_type == "superadvisor" and not self.is_superuser

    @property
    def is_expert(self):
        """
        True if user_type is in ["administrator", "manager", "advisor"]
        """
        return self.is_advisor or self.is_manager or self.is_administrator

    @property
    def is_client(self):
        """
        True if user_type is "client"
        """
        return self.user_type == "client"

    @property
    def is_professional(self):
        """
        True if user_type is "professional"
        """
        return self.user_type == "professional"

    @property
    def is_contact(self):
        """
        False
        """
        return False

    @property
    def is_user(self):
        """
        True
        """
        return True

    @property
    def is_admin(self):
        """
        True if user is superuser
        """
        return self.is_superuser

    @property
    def full_name(self):
        """
        Return display name as 'first_name last_name'
        """
        if self.first_name:
            return f"{self.first_name} {self.last_name}"
        return f"{self.last_name}"

    def __str__(self):
        """
        Return string as 'first_name last_name (email)'
        """
        if self.first_name:
            return f"({self.pk}) {self.first_name} {self.last_name} ({self.email})"
        return f"({self.pk}) {self.last_name} ({self.email})"

    def send_email(  # NOQA: CFQ002
        self,
        subject: str,
        html_message: str = None,
        context: dict = None,
        sender=None,
        as_background_task=True,
        use_fallback: bool = True,
        attachments: list = None,
        system_wide_smtp_server=False,
    ):
        """
        Sends an email to this User.

        :subject: mail subject
        :html_message: mail content as html text
        :context: context for template generation
        :sender: sender of the message
        :attachments: list of files described as { filename, content, mimetype }
             with content encoded as quopri.decodestring(raw_content)
        :system_wide_smtp_server: force default stmp server
        """
        context = context if context is not None else {}

        email_to_user_helper = EmailToUserHelper(account=self)
        task = email_to_user_helper.send_email(
            subject=subject,
            message=html_message,
            context=context,
            sender=sender,
            as_background_task=as_background_task,
            use_fallback=use_fallback,
            attachments=attachments,
            system_wide_smtp_server=system_wide_smtp_server,
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
        """
        context = context if context is not None else {}
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
        """
        True if user_type in ["administrator", "manager", "advisor", "client", "professional"]
        and is_active=True and group.is_active=True if group
        """
        if not self.is_active:
            return False

        if self.group is not None and not self.group.is_active:
            return False

        return self.user_type in [
            "administrator",
            "manager",
            "advisor",
            "superadvisor",
            "client",
            "professional",
        ]

    def send_initialize_account_url(self) -> int:
        """
        Send url for initializing account password
        """
        if self.email is None or self.email == "":
            return

        if self.group is not None and not self.group.is_active:
            return

        current_site = self.user_site()

        context = {
            "email": self.email,
            "domain": current_site.domain,
            "site_name": current_site.name,
            "uid": urlsafe_base64_encode(f"{self.pk}".encode("ascii")),
            "user": self,
            "token": default_token_generator.make_token(self),
            "protocol": "http",
        }
        subject = loader.render_to_string(
            "init_account/password_initialize_subject.html", context
        )
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        message_html = loader.render_to_string(
            "init_account/password_initialize_email-html.html", context
        )

        return self.send_email(
            subject=subject, html_message=message_html, system_wide_smtp_server=True
        )

    def send_reset_password_url(self) -> int:
        """
        Send url for reseting account password
        """
        if self.email is None or self.email == "":
            return

        if not self.can_login and self.last_login is not None:
            return

        current_site = self.user_site()

        context = {
            "email": self.email,
            "domain": current_site.domain,
            "site_name": current_site.name,
            "uid": urlsafe_base64_encode(f"{self.pk}".encode("ascii")),
            "user": self,
            "token": default_token_generator.make_token(self),
            "protocol": "http",
        }

        subject = loader.render_to_string(
            "registration/password_reset_subject.html", context
        )
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        message_html = loader.render_to_string(
            "registration/password_reset_email-html.html", context
        )

        return self.send_email(
            subject=subject, html_message=message_html, system_wide_smtp_server=True
        )

    @property
    def last_rgpd_consent(self) -> RgpdConsent:
        return (
            RgpdConsent.objects.filter(user__pk=self.pk)
            .order_by("-creation_date")
            .first()
        )

    @property
    def allow_to_use_email_to_send_reminder(self) -> bool:
        if self.last_rgpd_consent is None:
            return False
        return self.last_rgpd_consent.allow_to_use_email_to_send_reminder

    @property
    def allow_to_use_phone_number_to_send_reminder(self) -> bool:
        if self.last_rgpd_consent is None:
            return False
        if self.phone is not None:
            return self.last_rgpd_consent.allow_to_use_phone_number_to_send_reminder
        else:
            return False

    @property
    def allow_to_share_my_information_with_my_advisor(self) -> bool:
        if self.last_rgpd_consent is None:
            return False
        return self.last_rgpd_consent.allow_to_share_my_information_with_my_advisor

    @property
    def allow_to_share_my_information_with_partners(self) -> bool:
        if self.last_rgpd_consent is None:
            return False
        return self.last_rgpd_consent.allow_to_share_my_information_with_partners

    @property
    def main_housing(self) -> Housing:
        return self.housing.filter(is_main_address=True, user__pk=self.pk).first()

    @property
    def territories(self):
        if self.is_manager or self.is_advisor:
            return self.group.territories.all()

        return []

    @property
    def group_users(self):
        """
        Returns a list of users from the user group, including user
        """
        if self.group:
            return self.group.users

        return []

    @property
    def allowed_methods_for_contact(self):
        """
        Return allowed methods for contacting this user
        """
        methods = []

        if self.allow_to_use_phone_number_to_send_reminder:
            methods.append("sms")

        if self.allow_to_use_email_to_send_reminder:
            methods.append("mail")

        return methods
