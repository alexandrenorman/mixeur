# -*- coding: utf-8 -*-
import os
import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel

from helpers.helpers import unique_filename_in_path

from .tag import Tag


class FileManager(models.Manager):
    """
    File manager for files to be handled quickly
    """


def directory_path(instance, filename):
    uid = f"{uuid.uuid4()}"
    dir_path = f"fac/files/{instance.owning_group_id}/{uid[0]}/{uid[:2]}/{uid}"
    valid_file = unique_filename_in_path(dir_path, filename)
    full_path = os.path.join(dir_path, valid_file)
    return full_path


class File(MixeurBaseModel):
    """
    File with note and tag
    """

    objects = FileManager()

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")

    owning_group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe propriétaire"),
        on_delete=models.CASCADE,
        null=False,
        related_name="files",
    )

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    # linked organization or contact (and maybe other models later on)
    linked_object = GenericForeignKey("content_type", "object_id")

    document = models.FileField(_("Document"), upload_to=directory_path, max_length=500)
    url = models.URLField(_("Document URL"), blank=True)
    pinned = models.BooleanField(verbose_name=_("Épinglé"), default=False)
    note = models.TextField(_("Note"), max_length=15000, blank=False)
    tags = models.ManyToManyField(
        to=Tag,
        related_name="linked_files",
        verbose_name=_("Tags"),
        help_text=_("Liste de tags"),
        blank=True,
    )

    def __str__(self):
        return f"{self.created_at} {self.object_id} {self.note}"
