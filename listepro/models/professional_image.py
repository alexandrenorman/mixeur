# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel

from .professional_production import ProfessionalProduction


def img_prof_path(instance, filename):
    return f"productions/{instance.id}/{filename}"


class ProfessionalImage(MixeurBaseModel):

    production = models.ForeignKey(
        ProfessionalProduction, on_delete=models.CASCADE, default=None
    )
    name = models.CharField(verbose_name=_("Nom de l'image"), max_length=256)
    cropped = models.ImageField(upload_to=img_prof_path, blank=True)
