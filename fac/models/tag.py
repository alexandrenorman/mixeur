from core.models import MixeurBaseModel
from django.db import models
from django.db.models import fields
from django.utils.translation import ugettext_lazy as _


class TagQueryset(models.QuerySet):
    def accessible_by(self, user):
        if user.is_administrator:
            return self

        return self.filter(owning_group=user.group)


class TagManager(models.Manager.from_queryset(TagQueryset)):
    def get_queryset(self):
        return super().get_queryset().order_by("name")


class Tag(MixeurBaseModel):
    class Meta:
        unique_together = ["owning_group", "name"]

    name = fields.CharField(_("Name"), max_length=100)
    description = fields.TextField(_("Description"), blank=True, null=True)
    owning_group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe propriétaire"),
        on_delete=models.CASCADE,
        null=False,
        related_name="tags",
    )

    objects = TagManager()
