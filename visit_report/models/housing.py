# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from core.models import MixeurBaseModel


class Housing(MixeurBaseModel):
    HOUSING_TYPES = (
        ("house", _("Maison")),
        ("condo", _("Copropriété")),
        ("building", _("Immeuble")),
        ("flat", _("Appartement")),
        ("other", _("Autre")),
    )
    OWNERSHIP_TYPES = (
        ("tenant", _("Locataire")),
        ("owner", _("Propriétaire occupant")),
        ("landlord", _("Propriétaire bailleur")),
        ("other", _("Autre")),
    )

    class Meta:
        verbose_name = _("Logement")

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True
    )

    contact_or_organization_id = models.PositiveIntegerField(blank=True, null=True)
    # linked organization or contact (and maybe other models later on)
    contact_entity = GenericForeignKey("content_type", "contact_or_organization_id")

    user = models.ForeignKey(
        "accounts.User",
        verbose_name=_("Contact"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="housing",
    )

    is_main_address = models.BooleanField(
        _("Utiliser comme adresse principale"), default=False
    )

    groups = models.ManyToManyField(
        "accounts.Group", verbose_name=_("Structures attachées à ce logement")
    )

    address = models.CharField(_("Adresse"), max_length=200, blank=True, null=True)

    address_more = models.CharField(
        _("Complément d'adresse"), max_length=200, blank=True, null=True
    )

    city = models.CharField(_("Ville"), max_length=100, blank=True, null=True)

    postcode = models.CharField(_("Code postal"), max_length=8, blank=True, null=True)

    inseecode = models.CharField(_("Code INSEE"), max_length=8, blank=True, null=True)

    housing_type = models.CharField(
        _("Type de logement"), choices=HOUSING_TYPES, default="house", max_length=20
    )

    ownership = models.CharField(
        _("Propriété"), choices=OWNERSHIP_TYPES, default="owner", max_length=20
    )

    area = models.PositiveIntegerField(_("Superficie (en m²)"), default=0)

    occupants_number = models.PositiveIntegerField(_("Nombre d'occupants"), default=0)

    note = models.TextField(_("Notes"), blank=True, null=True)

    year = models.CharField(
        _("Année de construction"), max_length=8, blank=True, null=True
    )

    ownership_other_label = models.CharField(
        _("Autre statut d'occupation"), max_length=50, blank=True, null=True
    )

    housing_type_other_label = models.CharField(
        _("Autre Type de logement"), max_length=50, blank=True, null=True
    )

    def __str__(self):
        return "%s" % (self.address)

    def clean(self):
        """
        Clean

        - a client can have only one main_address -> other main_address are retrograded
        """
        if self.is_main_address:
            if (
                self.__class__.objects.filter(
                    contact_or_organization_id=self.contact_or_organization_id,
                    content_type=self.content_type,
                    is_main_address=True,
                )
                .exclude(pk=self.pk)
                .exists()
            ):
                for housing in self.__class__.objects.filter(
                    contact_or_organization_id=self.contact_or_organization_id,
                    content_type=self.content_type,
                    is_main_address=True,
                ).exclude(pk=self.pk):
                    housing.is_main_address = False
                    housing.save()
