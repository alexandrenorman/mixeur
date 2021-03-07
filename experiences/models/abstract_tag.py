# -*- coding: utf-8 -*-
from core.models import MixeurBaseModel
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractTagQueryset(models.QuerySet):
    def accessible_by(self, user):
        if user.is_administrator:
            return self

        return self.filter(owning_group=user.group)


class AbstractTagManager(models.Manager.from_queryset(AbstractTagQueryset)):
    def get_queryset(self):
        return super().get_queryset().order_by("name")


class AbstractTag(MixeurBaseModel):
    class Meta:
        abstract = True
        unique_together = ["owning_group", "name"]
        ordering = ["name"]

    objects = AbstractTagManager()

    name = models.CharField(_("Nom"), max_length=100)
    description = models.TextField(_("Description"), blank=True, null=True)
    owning_group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe propriétaire"),
        on_delete=models.CASCADE,
        null=False,
    )
    is_active = models.BooleanField(
        _("active"), default=True, help_text=_("Tag actif ?")
    )
