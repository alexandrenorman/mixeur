from core.models import MixeurBaseModel

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Status(MixeurBaseModel):
    name = models.CharField(verbose_name=_("Nom"), max_length=255)
    folder_model = models.ForeignKey(
        "fac.FolderModel", on_delete=models.CASCADE, related_name="statuses"
    )
    order = models.PositiveSmallIntegerField(_("Ordre"), default=0)
    color = models.CharField(default="#000000", verbose_name=_("Couleur"), max_length=7)

    def __str__(self):
        return f"{self.name} [{self.folder_model.name}]"

    class Meta:
        ordering = ["order"]
