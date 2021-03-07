# -*- coding: utf-8 -*-
from django.db import models
from core.models import MixeurBaseModel

from django.utils.translation import ugettext_lazy as _

from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from ckeditor.fields import RichTextField


# leaves function to not break migrations
def validation_absolute_positive(value):
    if value < 1:
        raise ValidationError(f"Value must be > 1 (was {value}")


class Diagnostic(MixeurBaseModel):
    class Meta:
        verbose_name = _("Diagnostic de copropriété")
        verbose_name_plural = _("Diagnostics de copropriétés")

    last_year = models.PositiveSmallIntegerField(
        _("Dernière année évaluée"), validators=(MinValueValidator(0),)
    )
    # OWNER
    user = models.ForeignKey(
        "accounts.user",
        related_name="diagnostic",
        verbose_name=_("Utilisateur associé à la demande"),
        on_delete=models.CASCADE,
    )
    # ADVISOR
    advisor = models.ForeignKey(
        "accounts.user",
        related_name="advised_diagnostic",
        verbose_name=_("Dernier Conseiller intervenant sur le diagnostic"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    # DATA
    copro = models.OneToOneField(
        "autodiag_copro.Copro",
        verbose_name=_("Informations générale"),
        on_delete=models.CASCADE,
    )
    # PARAMS
    params = models.OneToOneField(
        "autodiag_copro.Params",
        verbose_name=_("Paramètres principaux"),
        on_delete=models.CASCADE,
    )

    comments = RichTextField(
        _("Commentaires"), null=True, blank=True
    )  # FIXME: Only for Advisor ?

    def __str__(self):
        return f"name:{self.copro.name} / user:{self.user} / date:{self.created_at}"
