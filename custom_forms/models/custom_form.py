# -*- coding: utf-8 -*-
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel


class CustomForm(MixeurBaseModel):
    class Meta:
        verbose_name = _("Formulaire personnalisé")
        verbose_name_plural = _("Formulaires personnalisés")
        # TODO unique_together = ("model", "anchor", "version", "projects", "action_models", "folder_models", "groups")

    model = models.CharField(_("Modèle"), blank=False, max_length=100)
    anchor = models.CharField(_("Ancre"), blank=False, max_length=100)
    version = models.IntegerField(_("Version"), default=0)
    description = models.TextField(verbose_name=_("Description"), blank=True)
    form = JSONField(
        _("Formulaire"),
        help_text="Use https://jsonformatter.curiousconcept.com/ to validate",
    )

    projects = models.ManyToManyField(
        related_name="custom_forms",
        to="fac.project",
        verbose_name="Projets",
        blank=True,
    )

    action_models = models.ManyToManyField(
        related_name="custom_forms",
        to="fac.actionmodel",
        verbose_name="Modèle d'action",
        blank=True,
    )

    folder_models = models.ManyToManyField(
        related_name="custom_forms",
        to="fac.foldermodel",
        verbose_name="Modèle de dossiers",
        blank=True,
    )

    groups = models.ManyToManyField(
        related_name="custom_forms",
        to="accounts.group",
        verbose_name="Groupes",
        blank=True,
    )
