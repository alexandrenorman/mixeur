# -*- coding: utf-8 -*-

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel

from fac.helpers import get_incomplete_fields_for_contact
from fac.helpers import get_incomplete_fields_for_organization


class IncompleteModelQueryset(models.QuerySet):
    def accessible_by(self, user):
        if user.is_administrator:
            return self

        return self.filter(owning_group=user.group)


class IncompleteModelManager(models.Manager.from_queryset(IncompleteModelQueryset)):
    pass


class IncompleteModel(MixeurBaseModel):
    class Meta:
        verbose_name = _("Objet incomplet")
        verbose_name_plural = _("Objets incomplets")
        unique_together = ("owning_group", "content_type", "object_id")

    objects = IncompleteModelManager()

    owning_group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe propriétaire"),
        on_delete=models.CASCADE,
        null=False,
        related_name="incomplete_model",
    )
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    incomplete_object = GenericForeignKey("content_type", "object_id")
    fields = ArrayField(
        models.CharField(max_length=100, blank=True),
    )

    @staticmethod
    def check_incomplete_model_and_save(obj):
        if obj.__class__.__name__ == "Contact":
            fields = get_incomplete_fields_for_contact(obj)

        if obj.__class__.__name__ == "Organization":
            fields = get_incomplete_fields_for_organization(obj)

        if obj.__class__.__name__ == "Folder":
            # TBD
            # fields = get_incomplete_fields_for_folder(obj)  # NOQA: E800
            fields = []

        if fields:
            if obj.incomplete_models.exists():
                im = obj.incomplete_models.first()
                im.fields = fields
                im.save()
            else:
                obj.incomplete_models.create(
                    owning_group=obj.owning_group, incomplete_object=obj, fields=fields
                )
            return True
        else:
            if obj.incomplete_models.exists():
                obj.incomplete_models.all().delete()

        return False
