# -*- coding: utf-8 -*-
import functools
import logging
from difflib import SequenceMatcher

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from core.models import MixeurBaseModel

import fac.static_data

from .file_import import FileImport
from .tag import Tag

logger = logging.getLogger(__name__)  # NOQA


class ContactQueryset(models.QuerySet):
    def accessible_by(self, user):
        if user.is_administrator:
            return self

        return self.filter(owning_group=user.group)


class ContactManager(models.Manager.from_queryset(ContactQueryset)):
    def valid(self):
        return self.filter(fileimport=None)

    def being_imported(self):
        return self.exclude(fileimport=None)


class Contact(MixeurBaseModel):
    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
        ordering = ["last_name"]

    objects = ContactManager()

    owning_group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe propriétaire"),
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="contacts",
    )

    client_account = models.ForeignKey(
        "accounts.User",
        verbose_name=_("Compte client"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="contacts",
    )

    civility = models.CharField(
        _("Civilité"), choices=fac.static_data.CIVILITIES, max_length=10, default="O"
    )

    first_name = models.CharField(_("Prénom"), max_length=255)

    last_name = models.CharField(_("Nom"), max_length=255)

    email = models.EmailField(_("Email"), blank=True, max_length=255)

    address = models.CharField(_("Adresse"), blank=True, max_length=255)

    town = models.CharField(_("Ville"), blank=True, max_length=255)

    zipcode = models.CharField(_("Code Postal"), blank=True, max_length=50)
    inseecode = models.CharField(_("Code INSEE"), blank=True, max_length=50)

    lat = models.DecimalField(_("Latitude"), default=0, max_digits=9, decimal_places=6)
    lon = models.DecimalField(_("Longitude"), default=0, max_digits=9, decimal_places=6)

    country = models.CharField(_("Pays"), blank=True, max_length=100)

    phone = PhoneNumberField(
        _("Numéro de téléphone"), max_length=100, blank=True, null=True
    )
    mobile_phone = PhoneNumberField(
        _("Numéro de mobile"), max_length=100, blank=True, null=True
    )
    fax = PhoneNumberField(_("Numéro de fax"), max_length=100, blank=True, null=True)

    phone_cache = models.CharField(
        _("Cache pour le numéro de téléphone"), blank=True, max_length=100
    )
    mobile_phone_cache = models.CharField(
        _("Cache pour le numéro de mobile"), blank=True, max_length=100
    )
    fax_cache = models.CharField(
        _("Cache pour le numéro de fax"), blank=True, max_length=100
    )

    tags = models.ManyToManyField(
        to=Tag,
        related_name="contacts",
        verbose_name=_("Tags"),
        help_text=_("Liste de tags"),
        blank=True,
    )

    referents = models.ManyToManyField(
        to="accounts.User",
        related_name="contact_referents",
        verbose_name=_("Référents"),
        help_text=_("Liste de référents"),
        blank=True,
    )

    accepts_newsletters = models.BooleanField(
        _("Accepte les newsletters"), default=True
    )

    confirmed = models.BooleanField(_("Contact confirmé dans phplist"), default=True)

    blacklisted = models.BooleanField(
        _("Mis en liste noire dans phplist"), default=False
    )

    fileimport = models.ForeignKey(
        FileImport,
        verbose_name=_("Lié à un fichier d'import"),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    appointments = GenericRelation(
        "dialogwatt.Appointment",
        related_query_name="contact",
        content_type_field="content_type",
        object_id_field="object_id",
    )
    folders = GenericRelation(
        "fac.Folder",
        related_query_name="contact",
        content_type_field="content_type",
        object_id_field="object_id",
    )
    files = GenericRelation(
        "fac.File",
        related_query_name="contact",
        content_type_field="content_type",
        object_id_field="object_id",
    )
    notes = GenericRelation(
        "fac.Note",
        related_query_name="contact",
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
        related_query_name="contact",
        content_type_field="content_type",
        object_id_field="object_id",
    )

    custom_form_data = JSONField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.phone:
            self.phone_cache = f"0{self.phone.national_number}"

        if self.mobile_phone:
            self.mobile_phone_cache = f"0{self.mobile_phone.national_number}"

        if self.fax:
            self.fax_cache = f"0{self.fax.national_number}"

        super().save(*args, **kwargs)

    def clean(self):
        if not self.first_name and not self.last_name and not self.email:
            raise ValidationError(
                _("Un contact doit au minimum avoir un Prénom, un Nom ou un Courriel")
            )

    @functools.lru_cache(maxsize=512)
    def get_header_as_csv_data(self):
        logger.debug(f"contacts.models.Contact.get_header_as_csv_data {self}")
        return [
            "id",
            "civility",
            "first_name",
            "last_name",
            "email",
            "address",
            "zipcode",
            "town",
            "country",
            "phone",
            "mobile_phone",
            "fax",
            "tags",
            "organizations_ids",
            "organizations_names",
        ]

    @functools.lru_cache(maxsize=512)
    def get_as_csv_data(self):
        logger.debug(f"contacts.models.Contact.get_as_csv_data {self}")
        from .member_of_organization import MemberOfOrganization

        lo = MemberOfOrganization.objects.filter(contact__pk=self.pk)
        organization_ids = " / ".join([str(x.organization.pk) for x in lo])
        organization_names = " / ".join([x.organization.name for x in lo])
        return [
            self.pk,
            self.civility,
            self.first_name,
            self.last_name,
            self.email,
            self.address,
            self.zipcode,
            self.town,
            self.country,
            self.phone,
            self.mobile_phone,
            self.fax,
            " / ".join([x.name for x in self.tags.all()]),
            organization_ids,
            organization_names,
        ]

    @functools.lru_cache(maxsize=512)
    def compare_with_another_contact(self, contact):
        logger.debug(
            f"contacts.models.Contact.compare_with_another_contact {self} {contact}"
        )
        s_nb = 0
        s_tot = 0
        for f in ["first_name", "last_name", "email"]:
            similaritie = SequenceMatcher(
                None,
                str(getattr(self, f)),
                str(getattr(contact, f)),
                autojunk=False,
            )
            ratio = similaritie.real_quick_ratio()
            if ratio > 0.80:
                s_nb = 0
                s_tot = 0
                for f in ["first_name", "last_name", "email"]:
                    similaritie = SequenceMatcher(
                        None,
                        str(getattr(self, f)),
                        str(getattr(contact, f)),
                        autojunk=False,
                    )
                    ratio = similaritie.ratio()
                    s_tot += ratio
                    s_nb += 1

                break

            s_tot += ratio
            s_nb += 1

        score = 1.0 * s_tot / s_nb
        return score

    @functools.lru_cache(maxsize=512)
    def get_address(self, for_organization=None):
        logger.debug(f"contacts.models.Contact.get_address {self} {for_organization}")
        addr = {
            "address": self.address,
            "zipcode": self.zipcode,
            "town": self.town,
            "country": self.country,
            "phone": self.phone,
            "fax": self.fax,
        }
        from .member_of_organization import MemberOfOrganization

        if for_organization is None:
            members = MemberOfOrganization.objects.filter(contact__pk=self.pk)
        else:
            members = MemberOfOrganization.objects.filter(
                contact__pk=self.pk, organization__pk=for_organization.pk
            )

        if len(members) == 0:
            return addr

        elif len(members) == 1:
            if members[0].use_address_from_organization:
                o = members[0].organization
                addr = {
                    "address": o.address,
                    "zipcode": o.zipcode,
                    "town": o.town,
                    "country": o.country,
                    "phone": o.phone,
                    "fax": o.fax,
                }
                if len(self.phone) > 0:
                    addr["phone"] = self.phone

                if len(self.fax) > 0:
                    addr["fax"] = self.fax

            return addr

        elif len(members) > 1:
            raise ValueError(
                f"Can not decide which address should I use from organisations members {members}"
            )

        return addr

    @functools.lru_cache(maxsize=512)
    def use_address_from_organization(self, organization=None):
        logger.debug(
            f"contacts.models.Contact.use_address_from_organization {self} {organization}"
        )
        from .member_of_organization import MemberOfOrganization

        try:
            moo = MemberOfOrganization.objects.get(
                organization__pk=organization.pk, contact__pk=self.pk
            )
        except AttributeError:
            return False
        except ObjectDoesNotExist:
            return False

        return moo.use_address_from_organization

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
            if li.is_contact_in(self):
                lists.append(li)

        return lists

    @property
    @functools.lru_cache(maxsize=512)
    def is_member_of_organization(self):
        from .member_of_organization import MemberOfOrganization

        moo = MemberOfOrganization.objects.filter(contact__pk=self.pk)
        if len(moo) > 0:
            return True

        return False

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
            "class": "Contact",
            "type": '<i class="fa fa-user" aria-hidden="true"></i>',
            "name": f"{self.first_name} {self.last_name}",
            "email": self.email,
            "organization": ", ".join(
                [str(mo.organization) for mo in self.memberoforganization_set.all()]
            ),
            "nb": "",
            "delete_node": can_delete_node,
            "delete_message": delete_message,
        }

        if not self.email:
            data["type"] = '<i class="fa fa-user false" aria-hidden="true"></i>'

        return data

    @property
    def phone_as_string(self):
        return self.convert_phone_as_string(self.phone)

    @property
    def mobile_phone_as_string(self):
        return self.convert_phone_as_string(self.mobile_phone)

    def convert_phone_as_string(self, phone):
        import phonenumbers

        try:
            p = phonenumbers.parse(phone, "FR")
        except phonenumbers.phonenumberutil.NumberParseException:
            return self.phone

        return ", ".join(
            [
                f"0{p.national_number}",
                f"+{p.country_code}{p.national_number}",
            ]
        )

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
    def is_expert(self):
        return False

    @property
    def is_client(self):
        return False

    @property
    def is_contact(self):
        return True

    @property
    def is_admin(self):
        return False

    @property
    def full_name(self):
        """
        Return display name as 'first_name last_name'
        """
        return f"{self.first_name} {self.last_name}"
