from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel


class Valorization(MixeurBaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Titre"), default="")
    act = models.BooleanField(verbose_name=_("Payer à l'acte"))
    amount = models.DecimalField(
        verbose_name=_("Montant à l'acte ou en €/h"), max_digits=10, decimal_places=2
    )
    type_valorization = models.ForeignKey(
        "fac.TypeValorization",
        verbose_name=_("Type de valorisation"),
        on_delete=models.CASCADE,
        related_name="valorization",
    )
    period = models.ForeignKey(
        "fac.Period",
        on_delete=models.CASCADE,
        related_name="valorizations",
        verbose_name="Période",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Valorisation")
        verbose_name_plural = _("Valorisations")
