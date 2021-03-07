# -*- coding: utf-8 -*-
import itertools

from django.db import models

from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from core.models import MixeurBaseModel


def places_directory_path(instance, filename):
    return "places/{0}/{1}".format(instance.id, filename)


class Place(MixeurBaseModel):
    class Meta:
        verbose_name = _("Lieu de conseil")
        verbose_name_plural = _("Lieux de conseil")
        ordering = ("name",)

    name = models.CharField(_("Nom"), blank=False, max_length=100)
    color = models.CharField(_("Color"), blank=False, max_length=10, default="#888888")
    slug = models.SlugField(_("Slug"), unique=True)

    groups = models.ManyToManyField(
        "accounts.group", verbose_name=_("Structures attachées à ce lieu")
    )
    selected_advisors = models.ManyToManyField(
        "accounts.user", verbose_name=_("Conseillers intervenant sur ce lieu")
    )
    presentation = models.TextField(
        verbose_name=_("Présentation du lieu"), blank=True, null=True
    )

    internal_presentation = models.TextField(
        verbose_name=_("Présentation du lieu à destination des conseillers"),
        blank=True,
        null=True,
    )

    phone = PhoneNumberField(
        _("Numéro de téléphone"), max_length=100, blank=True, null=True
    )

    is_active = models.BooleanField(
        _("active"), default=True, help_text=_("Lieu actif ?")
    )

    address = models.CharField(_("Adresse"), max_length=200, blank=True, null=True)

    city = models.CharField(_("Ville"), max_length=100, blank=True, null=True)

    postcode = models.CharField(_("Code postal"), max_length=8, blank=True, null=True)

    lat = models.DecimalField(_("Latitude"), default=0, max_digits=9, decimal_places=6)
    lon = models.DecimalField(_("Longitude"), default=0, max_digits=9, decimal_places=6)

    inseecode = models.CharField(_("Code INSEE"), max_length=8, blank=True, null=True)

    url = models.URLField(_("Url"))
    email = models.EmailField(_("Courriel"), blank=True, null=True)

    img = models.ImageField(upload_to=places_directory_path, blank=True, null=True)

    @property
    def territories(self):
        """
        Returns territories from groups members
        """
        territories = [
            x.territories.all()
            for x in self.groups.prefetch_related("territories").all()
        ]
        merged_and_unique = list(set(list(itertools.chain(*territories))))
        return merged_and_unique

    @property
    def advisors(self):
        """
        Returns users whose place belongs to groups
        """
        users = [x.users for x in self.groups.all()]
        merged = list(itertools.chain(*users))
        return merged
