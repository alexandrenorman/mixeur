# -*- coding: utf-8 -*-
import functools
import logging

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from core.models import MixeurBaseModel

import fac.static_data

from helpers.models import representation_helper

from .file_import import FileImport
from .tag import Tag

logger = logging.getLogger(__name__)  # NOQA


class OrganizationQueryset(models.QuerySet):
    def accessible_by(self, user):
        if user.is_administrator:
            return self

        return self.filter(owning_group=user.group)


class OrganizationManager(models.Manager.from_queryset(OrganizationQueryset)):
    """"""

    def valid(self):
        return self.filter(fileimport=None)

    def being_imported(self):
        return self.exclude(fileimport=None)


@representation_helper
class Organization(MixeurBaseModel):
    """"""

    class Meta:
        verbose_name = _("Structure")
        verbose_name_plural = _("Structures")
        ordering = ["name"]

    objects = OrganizationManager()

    owning_group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe propriétaire"),
        on_delete=models.CASCADE,
        null=False,
        related_name="organisations",
    )

    type_of_organization = models.CharField(
        _("Type d'organisation"),
        choices=fac.static_data.TYPE_OF_ORGANIZATION,
        default="UNKNOWN",
        max_length=50,
    )

    name = models.CharField(_("Nom"), max_length=255)

    description = models.TextField(
        _("Description"),
        max_length=20000,
        blank=True,
    )

    reference = models.CharField(
        _("Référence"), help_text=_("Référence interne"), max_length=255, blank=True
    )

    address = models.CharField(_("Adresse"), max_length=255, blank=True)

    town = models.CharField(_("Ville"), max_length=255, blank=True)

    zipcode = models.CharField(_("Code postal"), max_length=50, blank=True)
    inseecode = models.CharField(_("Code INSEE"), blank=True, max_length=50)

    lat = models.DecimalField(_("Latitude"), default=0, max_digits=9, decimal_places=6)
    lon = models.DecimalField(_("Longitude"), default=0, max_digits=9, decimal_places=6)

    country = models.CharField(_("Pays"), max_length=100, blank=True)

    email = models.EmailField(_("Email"), blank=True, max_length=255)
    website = models.URLField(_("Site WEB"), blank=True, max_length=255)
    phone = PhoneNumberField(
        _("Numéro de téléphone"), max_length=100, blank=True, null=True
    )
    fax = PhoneNumberField(_("Numéro de fax"), max_length=100, blank=True, null=True)
    phone_cache = models.CharField(
        _("Cache pour le numéro de téléphone"), blank=True, max_length=100
    )
    fax_cache = models.CharField(
        _("Cache pour le numéro de fax"), blank=True, max_length=100
    )
    tags = models.ManyToManyField(
        to=Tag,
        related_name="organizations",
        verbose_name=_("Tags"),
        help_text=_("Liste de tags"),
    )
    referents = models.ManyToManyField(
        to="accounts.User",
        related_name="organization_referents",
        verbose_name=_("Réferents"),
        help_text=_("Liste de référents"),
    )

    accepts_newsletters = models.BooleanField(
        _("Accepte les newsletters"), default=True
    )

    fileimport = models.ForeignKey(
        FileImport,
        verbose_name=_("Lié à un fichier d'import"),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    folders = GenericRelation(
        "fac.Folder",
        related_query_name="organization",
        content_type_field="content_type",
        object_id_field="object_id",
    )
    files = GenericRelation(
        "fac.File",
        related_query_name="organization",
        content_type_field="content_type",
        object_id_field="object_id",
    )
    notes = GenericRelation(
        "fac.Note",
        related_query_name="organization",
        content_type_field="content_type",
        object_id_field="object_id",
    )
    ecorenover_simulations = GenericRelation(
        "fac.EcorenoverSimulation",
        related_query_name="contact",
        content_type_field="content_type",
        object_id_field="object_id",
    )

    incomplete_models = GenericRelation(
        "fac.IncompleteModel",
        related_query_name="organization",
        content_type_field="content_type",
        object_id_field="object_id",
    )

    custom_form_data = JSONField(blank=True, null=True)

    @property
    def verbose_name(self):
        return self._meta.verbose_name

    def __str__(self):
        return self.name

    @functools.lru_cache(maxsize=512)
    def get_contacts(self):
        logger.debug(f"contacts.models.Organization.get_contacts {self}")
        from .member_of_organization import MemberOfOrganization

        return [
            x.contact
            for x in MemberOfOrganization.objects.filter(organization__pk=self.pk)
        ]

    @functools.lru_cache(maxsize=512)
    def get_nb_contacts(self):
        logger.debug(f"contacts.models.Organization.get_nb_contacts {self}")
        return len(self.get_contacts())

    def get_duration_by_project(self):
        projects = {}
        for folder in self.folders.all():
            project = folder.model.project
            if not project.custom_display_fields.get("duration"):
                continue
            if project.pk not in projects:
                projects[project.pk] = {
                    "name": project.name,
                    "duration": 0,
                }
            projects[project.pk]["duration"] += folder.get_duration()
        return projects

    @functools.lru_cache(maxsize=512)
    def get_lists(self):
        from fac.models import List

        lists = []
        for li in List.objects.all():
            if self in li.get_organizations():
                lists.append(li)

        return lists

    @functools.lru_cache(maxsize=512)
    def is_contact_in(self, contact):
        """
        return True if a given contact is included in :
        - organisation
        """
        from .member_of_organization import MemberOfOrganization

        try:
            MemberOfOrganization.objects.get(
                organization__pk=self.pk, contact__pk=contact.pk
            )
        except Exception:
            return False

        return True

    @functools.lru_cache(maxsize=512)
    def get_header_as_csv_data(self):
        logger.debug(f"contacts.models.Organization.get_header_as_csv_data {self}")
        return [
            "id",
            "type_of_organization",
            "name",
            "address1",
            "address2",
            "address3",
            "zipcode",
            "town",
            "country",
            "email",
            "website",
            "phone",
            "fax",
            "tags",
            "referent",
            "created_at",
            "updated_at",
        ]

    def get_as_csv_data(self):
        logger.debug(f"contacts.models.Organization.get_as_csv_data {self}")
        return [
            self.pk,
            self.type_of_organization,
            self.name,
            self.address1,
            self.address2,
            self.address3,
            self.zipcode,
            self.town,
            self.country,
            self.email,
            self.website,
            self.phone,
            self.fax,
            " / ".join([x.name for x in self.tags.all()]),
            " / ".join([x.name for x in self.referent.all()]),
            self.created_at,
            self.updated_at,
        ]

    @functools.lru_cache(maxsize=512)
    def get_tree_data(self, parent_node=None, can_delete_node=True):
        if parent_node:
            node = f"{parent_node}.{self.pk}"
        else:
            node = f"{self.pk}"

        if can_delete_node:
            delete_message = ""
        else:
            delete_message = f"Delete parent {parent_node}"

        data = {
            "id": node,
            "pk": self.pk,
            "class": "Organization",
            "type": '<i class="fa fa-users" aria-hidden="true"></i>',
            "name": f"{self.name}",
            "email": self.email,
            "organization": "",
            "nb": len(self.get_contacts()),
            "delete_node": can_delete_node,
            "delete_message": delete_message,
            "data": [
                x.get_tree_data(parent_node=node, can_delete_node=False)
                for x in self.get_contacts()
            ],
            "open": False,
        }

        if not self.email:
            data["type"] = '<i class="fa fa-users false" aria-hidden="true"></i>'

        return data

    def save(self, *args, **kwargs):
        if self.phone:
            self.phone_cache = f"0{self.phone.national_number}"

        if self.fax:
            self.fax_cache = f"0{self.fax.national_number}"

        super().save(*args, **kwargs)
