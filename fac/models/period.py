from datetime import date
from core.models import MixeurBaseModel

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Period(MixeurBaseModel):
    name = models.CharField(verbose_name=_("Nom"), max_length=255)
    date_start = models.DateField(
        verbose_name=_("Début de période"), default=date.today
    )
    date_end = models.DateField(
        verbose_name=_("Date de fin de période"), default=date.today
    )

    def __str__(self):
        return self.name

    def contains(self, date_action: date):
        return self.date_start <= date_action <= self.date_end

    class Meta:
        verbose_name = _("Période")
        verbose_name_plural = _("Périodes")
