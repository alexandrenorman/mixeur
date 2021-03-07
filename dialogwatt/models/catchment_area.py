# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel

from territories.models import Commune


class CatchmentArea(MixeurBaseModel):
    class Meta:
        verbose_name = _("Zone de chalandise")
        verbose_name_plural = _("Zones de chalandise")
        ordering = ("name",)

    is_active = models.BooleanField(
        _("active"), default=True, help_text=_("Zone de chalandise active ?")
    )

    name = models.CharField(_("Nom"), blank=False, max_length=100)
    territories = models.ManyToManyField(Commune, verbose_name=_("Territoires"))
    group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe"),
        help_text=_("Groupe"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="catchment_area",
    )
    description = models.TextField(  # NOQA: DJ01
        _("Description"), blank=True, null=True
    )
    additionnal_information = models.TextField(  # NOQA: DJ01
        verbose_name=_(
            "Information complémentaire pour les CIE lors de l'accueil téléphonique"
        ),
        blank=True,
        null=True,
    )
