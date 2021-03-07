# -*- coding: utf-8 -*-
import csv
import functools
import io
import logging

from core.models import MixeurBaseModel
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .contact import Contact
from .organization import Organization
from .tag import Tag

logger = logging.getLogger(__name__)  # NOQA


class List(MixeurBaseModel):
    class Meta:
        verbose_name = _("Liste de contacts")
        verbose_name_plural = _("Listes de contacts")

    owning_group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe propriétaire"),
        on_delete=models.CASCADE,
        null=False,
        related_name="lists",
    )

    title = models.CharField(
        _("Nom de la liste"), max_length=200, blank=True, default=""
    )
    description = models.TextField(
        _("Description"), blank=True, max_length=500, default=""
    )
    use_organizations_as_contacts = models.BooleanField(
        _("Utiliser les organisations comme destinataires"),
        default=True,
        help_text=_(
            "Si cette case est cochée, les adresses mails "
            "des organisations seront incluses dans la liste, "
            "dans le cas contraire, seules les adresses des "
            "contacts des organisations seront prises en compte"
        ),
    )
    # list of contacts
    contacts = models.ManyToManyField(Contact, blank=True, verbose_name=_("Contacts"))
    # list of organizations
    organizations = models.ManyToManyField(
        Organization,
        verbose_name=_("Organisations"),
        help_text=_(
            "l'ensemble des contacts des organisations sélectionnées sera inclus dans la liste de diffusion"
        ),
        blank=True,
    )
    # list of lists
    lists = models.ManyToManyField(
        "List",
        verbose_name=_("Listes"),
        help_text=_(
            "l'ensemble des contacts des listes sélectionnées sera inclus dans la liste de diffusion"
        ),
        blank=True,
    )
    # Add list tags
    tags = models.ManyToManyField(
        to=Tag,
        related_name="lists",
        verbose_name=_("Tags"),
        help_text=_(
            "l'ensemble des contacts taggués avec ces tags seront inclus dans la liste de diffusion"
        ),
        blank=True,
    )

    def __str__(self):
        return "{} - {}".format(self.pk, self.title)

    @property
    def nb_contacts(self):
        return len(self.get_contacts())

    def get_contacts(self, already_checked_list_pks=None):
        """
        Return contacts for this list

        contacts are :
        - individual contacts
        - individuals from organisations or organisations
        """
        logger.debug(f"list.models.List.get_contacts {self}")
        contacts = list(self.contacts.all())

        for tag in self.tags.all():
            contacts += list(Contact.objects.filter(tags__in=[tag.pk]))
            for o in Organization.objects.filter(tags__in=[tag.pk]):
                if self.use_organizations_as_contacts:
                    contacts.append(o)
                else:
                    contacts += list(o.get_contacts())

        orga_contacts = list(self.organizations.all())

        if self.use_organizations_as_contacts:
            contacts += orga_contacts
        else:
            for oc in orga_contacts:
                contacts += oc.get_contacts()

        if not already_checked_list_pks:
            already_checked_list_pks = []
        already_checked_list_pks.append(self.pk)
        # Prevent recursion...
        other_lists = list(self.lists.exclude(pk__in=already_checked_list_pks))

        for lc in other_lists:
            contacts = contacts + lc.get_contacts(already_checked_list_pks)

        # Remove duplicate contacts
        filtered_contacts = []
        for c in contacts:
            if c not in filtered_contacts:
                filtered_contacts.append(c)

        return filtered_contacts

    @functools.lru_cache(maxsize=512)
    def get_children(self):
        """"""
        logger.debug(f"list.models.List.get_children {self}")
        children = []
        for c in self.contacts.all().order_by("last_name", "first_name"):
            children.append(c)

        for o in self.organizations.all().order_by("name"):
            children.append({"organization": o, "children": o.get_contacts()})

        for t in self.tags.all().order_by("name"):
            children.append({"tag": t, "children": t.get_contacts()})

        for li in self.lists.exclude(pk=self.pk):
            children.append({"list": li, "children": li.get_children()})

        return children

    @functools.lru_cache(maxsize=512)
    def is_contact_in(self, contact):
        """
        return True if a given contact is included in :
        - individual contacts
        - organisations
        - other lists
        """
        logger.debug(f"list.models.List.is_contact_in {self} {contact}")

        if contact in self.contacts.all():
            return True

        for o in self.get_organizations():
            if o.is_contact_in(contact):
                return True

        for li in self.get_lists():
            if li != self:
                if li.is_contact_in(contact):
                    return True

        return False

    @functools.lru_cache(maxsize=512)
    def get_organizations(self):
        """
        Return organizations for this list

        organizations are :
        - organisations
        - other lists
        """
        logger.debug(f"list.models.List.get_organizations {self}")
        organizations = []

        try:
            orga_organizations = [x for x in self.organizations.all()]
        except ValueError:
            orga_organizations = []

        try:
            # Prevent recursion...
            list_organizations = [x for x in self.lists.exclude(pk=self.pk)]
        except ValueError:
            list_organizations = []

        organizations += orga_organizations

        for lc in list_organizations:
            organizations += lc.get_organizations()

        organizations += Organization.objects.filter(
            tags__in=[x.pk for x in self.tags.all()]
        )

        filtered_organizations = []
        for c in organizations:
            if c not in filtered_organizations:
                filtered_organizations.append(c)

        return filtered_organizations

    @functools.lru_cache(maxsize=512)
    def get_lists(self):
        """
        Return all lists included in this list
        """
        logger.debug(f"list.models.List.get_lists {self}")
        lists = [self]
        for x in self.lists.all():
            for li in x.get_lists():
                lists.append(li)

        return lists

    @functools.lru_cache(maxsize=512)
    def get_contacts_as_csv(self):
        logger.debug(f"list.models.List.get_contacts_as_csv {self}")
        output = io.StringIO()
        writer = csv.writer(
            output, quoting=csv.QUOTE_NONNUMERIC, delimiter="\t", quotechar='"'
        )
        header = False
        for c in self.get_contacts():
            if not header:
                header = True
                writer.writerow(c.get_header_as_csv_data())

            writer.writerow(c.get_as_csv_data())

        return output.getvalue()

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

        data_organizations = {
            "id": f"{node}.O",
            "pk": self.pk,
            "class": "Organization",
            "type": '<i class="fa fa-users" aria-hidden="true"></i>',
            "name": _("Organisations"),
            "email": "",
            "organization": "",
            "nb": 0,
            "delete_node": False,
            "delete_message": delete_message,
            "data": [
                x.get_tree_data(
                    parent_node=node + ".O", can_delete_node=can_delete_node
                )
                for x in self.organizations.all()
            ],
            "open": False,
        }
        for d in data_organizations["data"]:
            data_organizations["nb"] += d["nb"]

        data_contacts = {
            "id": f"{node}.C",
            "pk": self.pk,
            "class": "Contact",
            "type": '<i class="fa fa-user" aria-hidden="true"></i>',
            "name": _("Contacts"),
            "email": "",
            "organization": "",
            "nb": 0,
            "delete_node": False,
            "delete_message": delete_message,
            "data": [
                x.get_tree_data(
                    parent_node=node + ".C", can_delete_node=can_delete_node
                )
                for x in self.contacts.all()
            ],
            "open": False,
        }
        data_contacts["nb"] = len(data_contacts["data"])

        data_tags = {
            "id": f"{node}.T",
            "pk": self.pk,
            "class": "Tag",
            "type": '<i class="fa fa-tag" aria-hidden="true"></i>',
            "name": _("Tags"),
            "email": "",
            "organization": "",
            "nb": 0,
            "delete_node": False,
            "delete_message": delete_message,
            "data": [
                x.get_tree_data(
                    parent_node=node + ".T", can_delete_node=can_delete_node
                )
                for x in self.tags.all()
            ],
            "open": False,
        }
        data_lists = {
            "id": f"{node}.L",
            "pk": self.pk,
            "class": "List",
            "type": '<i class="fa fa-list" aria-hidden="true"></i>',
            "name": _("Listes"),
            "email": "",
            "organization": "",
            "nb": 0,
            "delete_node": False,
            "delete_message": delete_message,
            "data": [
                x.get_tree_data(
                    parent_node=node + ".L", can_delete_node=can_delete_node
                )
                for x in self.lists.all()
            ],
            "open": False,
        }

        nb = 0
        # for i in subdata:
        #    nb += int(i['nb'])

        data = {
            "id": node,
            "pk": self.pk,
            "class": "List",
            "type": '<i class="fa fa-list" aria-hidden="true"></i>',
            "name": "{}".format(self.title),
            "email": "",
            "organization": "",
            "nb": nb,
            "delete_node": can_delete_node,
            "delete_message": delete_message,
            "data": [],
            "open": False,
        }

        for li in [data_organizations, data_contacts, data_tags, data_lists]:
            if len(li["data"]) > 0:
                data["data"].append(li)

        return data
