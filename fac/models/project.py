from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import BooleanField
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel


class ProjectQueryset(models.QuerySet):
    def accessible_by(self, user):
        if user.is_administrator:
            return self

        groups = [user.group] + list(user.group.laureate_groups.all())
        return self.filter(groups__in=groups)


class ProjectManager(models.Manager.from_queryset(ProjectQueryset)):
    pass


class Project(MixeurBaseModel):
    objects = ProjectManager()

    name = models.TextField(verbose_name=_("Description"), default="")
    groups = models.ManyToManyField(
        "accounts.Group",
        related_name="group_projects",
        blank=True,
        help_text=_(
            "Ce champs doit être édité manuellement uniquement si vous ne "
            "renseignez pas de type de valorization."
        ),
    )
    type_valorizations = models.ManyToManyField(
        "fac.TypeValorization", related_name="type_valorization_projects", blank=True
    )

    # configurations specific to the project
    is_actimmo = models.BooleanField(default=False, verbose_name=_("Project ACTIMMO ?"))

    # configurations of contacts linked to a FolderModel of this Project
    is_contact_first_name_mandatory = models.BooleanField(
        default=False, verbose_name=_("Les contacts liés doivent avoir un prénom")
    )
    is_contact_last_name_mandatory = models.BooleanField(
        default=False, verbose_name=_("Les contacts liés doivent avoir un nom")
    )
    is_contact_email_mandatory = models.BooleanField(
        default=False, verbose_name=_("Les contacts liés doivent avoir un email")
    )
    is_contact_address_mandatory = models.BooleanField(
        default=False, verbose_name=_("Les contacts liés doivent avoir une adresse")
    )
    is_contact_phone_mandatory = models.BooleanField(
        default=False,
        verbose_name=_("Les contacts liés doivent avoir un numéro de téléphone"),
    )
    is_contact_mobile_phone_mandatory = models.BooleanField(
        default=False,
        verbose_name=_("Les contacts liés doivent avoir numéro de téléphone mobile"),
    )
    is_contact_tags_mandatory = models.BooleanField(
        default=False, verbose_name=_("Les contacts liés doivent avoir au moins un tag")
    )
    is_contact_referents_mandatory = models.BooleanField(
        default=False,
        verbose_name=_("Les contacts liés doivent avoir au moins un référent"),
    )
    # configurations of organizations linked to a FolderModel of this Project
    is_organization_email_mandatory = models.BooleanField(
        default=False, verbose_name=_("Les structures liées doivent avoir un email")
    )
    is_organization_description_mandatory = models.BooleanField(
        default=False,
        verbose_name=_("Les structures liées doivent avoir une description"),
    )
    is_organization_reference_mandatory = models.BooleanField(
        default=False,
        verbose_name=_("Les structures liées doivent avoir une référence"),
    )
    is_organization_website_mandatory = models.BooleanField(
        default=False, verbose_name=_("Les structures liées doivent avoir un site web")
    )
    is_organization_address_mandatory = models.BooleanField(
        default=False, verbose_name=_("Les structures liées doivent avoir une adresse")
    )
    is_organization_phone_mandatory = models.BooleanField(
        default=False,
        verbose_name=_("Les structures liées doivent avoir un numéro de téléphone"),
    )
    is_organization_tags_mandatory = models.BooleanField(
        default=False,
        verbose_name=_("Les structures liées doivent avoir au moins un tag"),
    )
    is_organization_referents_mandatory = models.BooleanField(
        default=False,
        verbose_name=_("Les structures liées doivent avoir au moins un référent"),
    )

    should_members_of_organization_respect_rules = models.BooleanField(
        default=False,
        verbose_name=_(
            "Les contacts membres d'une structure liée doivent respecter les règles du projet"
        ),
    )

    can_entities_have_multiple_folders_of_same_type = models.BooleanField(
        default=True,
        verbose_name=_(
            "Les entités du orojet peuvent créer plusieurs dossiers avec le même modèle"
        ),
    )

    custom_display_fields = JSONField(
        blank=True,
        null=True,
        default=dict,
        verbose_name=_("Champs à afficher dans l'écran des statistiques et l'export"),
    )

    custom_form_data = JSONField(blank=True, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_organization_field_requirements(cls):
        return {
            field.name[len("is_organization_") :]: field.name  # noqa: E203
            for field in cls._meta.fields
            if isinstance(field, BooleanField)
            and field.name.startswith("is_organization_")
        }

    @classmethod
    def get_contact_field_requirements(cls):
        return {
            field.name[len("is_contact_") :]: field.name  # noqa: E203
            for field in cls._meta.fields
            if isinstance(field, BooleanField) and field.name.startswith("is_contact_")
        }

    class Meta:
        verbose_name = _("Projet")
        verbose_name_plural = _("Projets")
