from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel


class ActionModel(MixeurBaseModel):
    name = models.CharField(verbose_name=_("Nom du modèle de l'action"), max_length=255)
    description = models.TextField(
        verbose_name=_("Description de l'action"), blank=True, default=""
    )
    trigger_status = models.ForeignKey(
        "Status",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="action_models",
    )
    category_model = models.ForeignKey(
        "fac.CategoryModel", on_delete=models.CASCADE, related_name="action_models"
    )
    default = models.BooleanField(
        default=False, verbose_name=(_("Action présente par défaut")), db_index=True
    )
    optional = models.BooleanField(
        default=False, verbose_name=(_("Action optionnelle")), db_index=True
    )
    should_generate_default_actions = models.BooleanField(
        default=True,
        verbose_name=(
            _(
                "Générer des actions par défaut dans les dossiers existants "
                "(si `Action présente par défaut` est cochée)"
            )
        ),
    )
    valorizations = models.ManyToManyField(
        "fac.Valorization",
        verbose_name=_("Valorisations"),
        related_name="action_models",
        blank=True,
    )
    order = models.PositiveSmallIntegerField(_("Ordre"), default=0)
    coefficient_enabled = models.BooleanField(
        default=False, verbose_name=_("Activer la répartition des valorisations")
    )

    message_required = models.BooleanField(
        default=False, verbose_name=(_("Commentaire requis"))
    )
    file_required = models.BooleanField(
        default=False, verbose_name=(_("Pièce jointe requise"))
    )
    contact_required = models.BooleanField(
        default=False, verbose_name=(_("Contact associé requis"))
    )

    disabled = models.BooleanField(
        default=False,
        verbose_name=(_("Désactiver")),
        help_text=(
            _(
                "L'interface ne permettra plus de créer d'actions de ce type, "
                + "mais les actions existantes ne seront pas supprimées."
            )
        ),
    )

    def __str__(self):
        return f"{self.category_model.folder_model.name} - {self.name}"

    class Meta:
        ordering = ["order"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(default=True) | models.Q(optional=True),
                name="default_or_optional",
            )
        ]
