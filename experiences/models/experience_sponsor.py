# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel

from .sponsor_tag import SponsorTag


class ExperienceSponsor(MixeurBaseModel):
    class Meta:
        verbose_name = _("Experience et sponsor")
        verbose_name_plural = _("Experiences et sponsors")
        # ordering = ["-date"]

    title = models.CharField(
        _("Nom du programme"), max_length=150, blank=False, null=False
    )
    contract_number = models.CharField(
        _("Numéro de contrat"), max_length=150, blank=False, null=False
    )
    sponsor = models.ForeignKey(
        SponsorTag,
        verbose_name=_("Financeur"),
        on_delete=models.CASCADE,
        null=False,
        related_name="experiences_sponsors",
    )
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    owning_group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe propriétaire"),
        on_delete=models.CASCADE,
        null=False,
        related_name="experiences_sponsor",
    )
