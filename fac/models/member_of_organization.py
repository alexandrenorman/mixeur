# -*- coding: utf-8 -*-
from core.models import MixeurBaseModel
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from helpers.models import representation_helper

from .contact import Contact
from .organization import Organization
from .tag import Tag


@representation_helper
class MemberOfOrganization(MixeurBaseModel):
    """"""

    class Meta:
        verbose_name = _("Membre d'organisations")
        verbose_name_plural = _("Membres d'organisations")
        ordering = ["contact__last_name"]

    owning_group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe propriétaire"),
        on_delete=models.CASCADE,
        null=False,
        related_name="member_of_organization",
    )

    # TODO: test if already such relation contact-organization exists
    contact = models.ForeignKey(
        Contact, verbose_name=_("Contact"), on_delete=models.CASCADE
    )
    organization = models.ForeignKey(
        Organization, verbose_name=_("Organisme"), on_delete=models.CASCADE
    )
    use_address_from_organization = models.BooleanField(
        _("Utiliser l'adresse de la structure"), default=False
    )
    title_in_organization = models.CharField(
        _("Titre dans l'organisation"), max_length=200, blank=True, default=""
    )
    tags = models.ManyToManyField(
        to=Tag,
        related_name="functions_of_member_of_organization",
        verbose_name=_("Fonction dans l'organisation (tag)"),
        help_text=_("Liste de tags"),
        blank=True,
    )
    competencies_tags = models.ManyToManyField(
        to=Tag,
        related_name="competencies_of_member_of_organization",
        verbose_name=_("Domaine de compétences / d'activités"),
        help_text=_("Liste de compétences"),
        blank=True,
    )
    destruction_date = models.DateTimeField(
        verbose_name=("Date de destruction"), blank=True, null=True, default=None
    )

    def clean(self, *args, **kwargs):
        other_orgs = (
            MemberOfOrganization.objects.filter(contact=self.contact)
            .filter(use_address_from_organization=True)
            .exclude(pk=self.pk)
        )
        if len(other_orgs) > 0 and self.use_address_from_organization:
            msg = _(
                "Un contact ne peut pas utiliser l'adresse de plusieurs structures en même temps."
                + "{}".format([x.organization.name for x in other_orgs])
            )
            raise ValidationError(msg)
        super(MemberOfOrganization, self).clean(*args, **kwargs)

    def __str__(self):
        return " ".join(
            [str(self.contact), str(self.organization), self.title_in_organization]
        )
