# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel

from .experience_sponsor import ExperienceSponsor
from .assignment_tag import AssignmentTag
from .experience_tag import ExperienceTag
from .job_tag import JobTag
from .partner_tag import PartnerTag
from .public_tag import PublicTag
from .year_tag import YearTag

import html2text


def experience_directory_path(instance, filename):
    return "experiences/{0}/{1}/{2}".format(
        instance.owning_group.pk, instance.pk, filename
    )


class Experience(MixeurBaseModel):
    class Meta:
        verbose_name = _("Experience")
        verbose_name_plural = _("Experiences")
        # ordering = ["-date"]

    owning_group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe propriétaire"),
        on_delete=models.CASCADE,
        null=False,
        related_name="experiences",
    )

    is_showcase = models.BooleanField(
        _("projet vitrine"), default=False, help_text=_("Projet vitrine")
    )

    title = models.CharField(_("Titre"), max_length=150)
    # date = models.DateField(verbose_name=_("Date de réalisation"),)
    description = models.TextField(
        verbose_name=_("Description"), blank=False, null=False
    )
    internal_reference = models.CharField(
        _("Référence interne"), max_length=150, blank=False, null=False
    )
    image1 = models.ImageField(
        upload_to=experience_directory_path,
        verbose_name=_("Illustration 1"),
        blank=True,
        null=True,
    )
    image2 = models.ImageField(
        upload_to=experience_directory_path,
        verbose_name=_("Illustration 2"),
        blank=True,
        null=True,
    )
    duration = models.PositiveIntegerField(
        verbose_name=_("Durée de réalisation (en jours)"), default=0
    )
    referent = models.ForeignKey(
        "accounts.User",
        verbose_name=_("Référent"),
        on_delete=models.CASCADE,
        null=False,
        related_name="experiences",
    )
    years = models.ManyToManyField(
        to=YearTag,
        related_name="experience_years",
        verbose_name=_("Années"),
        blank=False,
    )
    sponsors = models.ManyToManyField(
        to=ExperienceSponsor,
        related_name="experience_sponsors",
        verbose_name=_("Financeurs"),
        blank=True,
    )
    jobs = models.ManyToManyField(
        to=JobTag,
        related_name="experience_jobs",
        verbose_name=_("Métiers"),
        blank=False,
    )
    publics = models.ManyToManyField(
        to=PublicTag,
        related_name="experience_publics",
        verbose_name=_("Publics"),
        blank=False,
    )
    tags = models.ManyToManyField(
        to=ExperienceTag,
        related_name="experience_tags",
        verbose_name=_("Tags"),
        blank=True,
    )

    budget = models.FloatField(_("Budget total (en €)"), default=0)
    budget_group = models.FloatField(_("Budget de la structure (en €)"), default=0)
    partners = models.ManyToManyField(
        to=PartnerTag,
        related_name="experience_partners",
        verbose_name=_("Partenaires"),
        blank=True,
    )
    role = models.TextField(
        verbose_name=_("Rôle de la structure"), blank=False, null=False
    )
    description_en = models.TextField(
        verbose_name=_("Description (en anglais)"), blank=True, null=True
    )
    url = models.URLField(_("Site Web"), blank=True, null=True)
    assignments = models.ManyToManyField(
        to=AssignmentTag,
        related_name="experience_assignments",
        verbose_name=_("Missions"),
        blank=True,
    )

    @property
    def description_as_ascii(self):
        return html2text.html2text(self.description)

    @property
    def description_en_as_ascii(self):
        return html2text.html2text(self.description_en)

    @property
    def role_as_ascii(self):
        return html2text.html2text(self.role)
