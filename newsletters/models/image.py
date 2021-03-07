# -*- coding: utf-8 -*-
import os
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel

from helpers.helpers import unique_filename_in_path


class ImageQueryset(models.QuerySet):
    def accessible_by(self, user):
        if user.is_administrator:
            return self

        return self.filter(group=user.group)


class ImageManager(models.Manager.from_queryset(ImageQueryset)):
    """"""

    def valid(self):
        return self.filter(fileimport=None)

    def being_imported(self):
        return self.exclude(fileimport=None)


def image_directory_path(instance, filename):
    uid = f"{uuid.uuid4()}"
    dir_path = f"newsletters/{instance.group.pk}/{uid[0]}/{uid[:2]}/{uid}"
    valid_file = unique_filename_in_path(dir_path, filename)
    full_path = os.path.join(dir_path, valid_file)
    return full_path


class Image(MixeurBaseModel):
    class Meta:
        verbose_name = _("Image")

    objects = ImageManager()

    group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe propriétaire"),
        on_delete=models.CASCADE,
        null=False,
        related_name="image",
    )

    image = models.FileField(
        _("Document"), upload_to=image_directory_path, max_length=500
    )
