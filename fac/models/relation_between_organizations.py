from core.models import MixeurBaseModel
from django.db import models
from django.utils.translation import ugettext_lazy as _
from fac.models import Organization


class RelationBetweenOrganizationQueryset(models.QuerySet):
    def accessible_by(self, user):
        if user.is_administrator:
            return self

        return self.filter(owning_group=user.group)


class RelationBetweenOrganizationManager(
    models.Manager.from_queryset(RelationBetweenOrganizationQueryset)
):
    pass


class RelationBetweenOrganization(MixeurBaseModel):
    """
    `first_organization` is `relation_name` of `second_organization`
    ex: `Hespul` est `la maison mère` de `MaSuperStructure`
    """

    class Meta:
        verbose_name = _("Relation entre structures")
        verbose_name_plural = _("Relations entre structures")

    objects = RelationBetweenOrganizationManager()

    owning_group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe propriétaire"),
        on_delete=models.CASCADE,
        null=False,
        related_name="relations_between_organizations",
    )

    first_organization = models.ForeignKey(
        Organization,
        verbose_name=_("Sujet de la relation"),
        help_text=_("ex: structure parente"),
        related_name="forward_relations",
        on_delete=models.CASCADE,
    )
    relation_name = models.CharField(
        _("Nom de la relation entre les structures"),
        help_text=_("ex: la maison mère"),
        max_length=100,
    )
    second_organization = models.ForeignKey(
        Organization,
        verbose_name=_("Objet de la relation"),
        related_name="backward_relations",
        help_text=_("ex: structure fille"),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return (
            f"{self.first_organization} est {self.relation_name}"
            f" de {self.second_organization}"
        )
