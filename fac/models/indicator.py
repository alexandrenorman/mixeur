from core.models import MixeurBaseModel

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Indicator(MixeurBaseModel):
    TYPES = [
        ("duration", _("Durée")),
        ("numbers", _("Nombre")),
        ("at_least_one", _("Au moins un")),
    ]

    action_models = models.ManyToManyField("fac.ActionModel", related_name="indicators")
    indicator_type = models.CharField(
        verbose_name=_("Type de l'indicateur"), choices=TYPES, max_length=15
    )

    def __str__(self):
        return "Indicateur {}".format(self.pk)

    class Meta:
        verbose_name = _("Indicateur")
        verbose_name_plural = _("Indicateurs")
