# -*- coding: utf-8 -*-
from core.models import MixeurBaseModel
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from helpers.models import representation_helper

from .tag import Tag
from .contact import Contact
from .organization import Organization


class NoteQueryset(models.QuerySet):
    def accessible_by(self, user):
        if user.is_administrator:
            return self

        return self.filter(owning_group=user.group)


class NoteManager(models.Manager.from_queryset(NoteQueryset)):
    pass


@representation_helper
class Note(MixeurBaseModel):
    """
    Note with date and tag
    """

    objects = NoteManager()

    class Meta:
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")

    owning_group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe propriétaire"),
        on_delete=models.CASCADE,
        null=False,
        related_name="notes",
    )

    creator = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        verbose_name=_("Createur"),
        blank=True,
        null=True,
    )

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    # linked organization or contact (and maybe other models later on)
    linked_object = GenericForeignKey("content_type", "object_id")

    note = models.TextField(_("Note"), max_length=15000, blank=False)
    pinned = models.BooleanField(verbose_name=_("Épinglée"), default=False)
    tags = models.ManyToManyField(
        to=Tag,
        related_name="linked_notes",
        verbose_name=_("Tags"),
        help_text=_("Liste de tags"),
        blank=True,
    )
    reminder = GenericRelation(
        "fac.Reminder",
        related_query_name="note",
        content_type_field="content_type_task",
        object_id_field="object_id_task",
    )

    def __str__(self):
        return f"{self.created_at} {self.note}"

    @property
    def note_linked_object_name(self):
        if type(self.linked_object) is Contact:
            return self.linked_object.full_name

        if type(self.linked_object) is Organization:
            return self.linked_object.name

        return ""
