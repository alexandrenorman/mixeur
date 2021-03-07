# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


from core.models import MixeurBaseModel

from territories.models import Commune

from white_labelling.models import WhiteLabelling


def group_directory_path(instance, filename):
    return f"groups/{instance.id}/{filename}"


class GroupManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class ActimmoGroupManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(pilot_groups__in=[Group.objects.get(name="CLER")])
        )


class Group(MixeurBaseModel):
    """"""

    class Meta:
        verbose_name = _("Groupe")
        verbose_name_plural = _("Groupes")

    objects = GroupManager()
    actimmo_groups = ActimmoGroupManager()

    ademe_id = models.CharField(
        verbose_name=_("ADEME_ID for SARE"),
        blank=True,
        default="",
        max_length=20,
    )
    name = models.CharField(_("Nom"), blank=False, max_length=50)
    slug = models.SlugField(_("Slug"), unique="true", blank=False)
    full_name = models.CharField(_("Nom complet"), blank=True, max_length=200)
    is_admin = models.BooleanField(
        _("Groupe régional d'administration"),
        default=False,
        help_text=_("Groupe utilisé pour gérer les groupes par région ?"),
    )
    admin_group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe administrateur"),
        help_text=_("Groupe parent qui gère l'administration"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="managed_groups",
    )
    pilot_groups = models.ManyToManyField(
        "accounts.Group",
        verbose_name=_("Structures pilotes"),
        help_text=_("Dans FAC, les structures pilotes de cette structures"),
        related_name="laureate_groups",
        blank=True,
    )
    is_active = models.BooleanField(
        _("active"), default=True, help_text=_("Active group ?")
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    profile_pic = models.ImageField(
        upload_to=group_directory_path,
        blank=True,
    )
    presentation = models.TextField(
        verbose_name=_("Présentation de la structure"),
        blank=True,
    )
    address = models.CharField(
        _("Adresse"),
        max_length=200,
        blank=True,
    )
    territories = models.ManyToManyField(Commune, verbose_name=_("Territoires"))
    phone = PhoneNumberField(
        _("Numéro de téléphone"), max_length=100, blank=True, null=True
    )
    email = models.EmailField(
        _("Courriel"),
        blank=True,
    )
    website = models.URLField(
        _("Site internet"),
        blank=True,
    )
    # Specific to FAC app
    coefficient = models.DecimalField(
        default=1,
        verbose_name=_("Coefficient de valorisation"),
        max_digits=4,
        decimal_places=3,
    )

    white_labelling = models.ForeignKey(
        "white_labelling.WhiteLabelling",
        verbose_name=_("Marque blanche préférée"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="group",
        limit_choices_to={"is_active": True},
    )

    def __str__(self):
        return f"{self.name}"

    @property
    def users(self):
        """
        Return users list which are members of this group
        """
        return list(self.profile.all())

    @property
    def users_count(self):
        """
        Return numper of users which are members of this group
        """
        return len(self.users)

    @property
    def preferred_white_labelling(self):
        """
        Return preferred white labelling for group or default WhiteLabelling
        """
        if self.white_labelling:
            return self.white_labelling

        default = WhiteLabelling.objects.filter(is_active=True, is_default=True)
        if default.exists():
            return default.first()

        return None

    @property
    def display_name(self):
        """
        Return full_name if defined
        """
        if self.full_name:
            return self.full_name
        return self.name

    def is_member(self, user):
        """
        Return True if user is member of this group
        """
        return user in self.users

    def clean(self):
        if self.is_admin and self.admin_group is not None:
            raise ValidationError(
                _(
                    "Un groupe d'administration ne peut pas être administré par un groupe."
                )
            )
        if (
            not self.is_admin
            and self.admin_group is not None
            and not self.admin_group.is_admin
        ):
            raise ValidationError(
                _(
                    "Un groupe standard doit être administré par un groupe d'administration."
                )
            )
