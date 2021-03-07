from core.models import MixeurBaseModel

from django.db import models
from django.utils.translation import ugettext_lazy as _


class CategoryModel(MixeurBaseModel):
    name = models.CharField(
        verbose_name=_("Nom du modèle de catégorie"), max_length=255
    )
    folder_model = models.ForeignKey(
        "fac.FolderModel", on_delete=models.CASCADE, related_name="categories"
    )
    order = models.PositiveSmallIntegerField(_("Ordre"), default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]
