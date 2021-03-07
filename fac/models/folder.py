from datetime import date

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel

from .type_valorization import TypeValorization


class FolderQueryset(models.QuerySet):
    def accessible_by(self, user):
        if user.is_administrator:
            return self

        return self.filter(owning_group=user.group)


class FolderManager(models.Manager.from_queryset(FolderQueryset)):
    def get_queryset(self):
        return super().get_queryset()


class Folder(MixeurBaseModel):
    description = models.TextField(
        verbose_name=_("Description"), default="", blank=True
    )
    model = models.ForeignKey(
        "fac.FolderModel", on_delete=models.CASCADE, related_name="folders"
    )
    owning_group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe propriétaire"),
        on_delete=models.CASCADE,
        related_name="folders",
    )
    type_valorization = models.ForeignKey(
        "fac.TypeValorization",
        on_delete=models.CASCADE,
        related_name="folders",
        blank=True,
        null=True,
    )

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    # linked organization or contact (and maybe other models later on)
    linked_object = GenericForeignKey("content_type", "object_id")

    incomplete_models = GenericRelation(
        "fac.IncompleteModel",
        related_query_name="folder",
        content_type_field="content_type",
        object_id_field="object_id",
    )

    custom_form_data = JSONField(blank=True, null=True)

    objects = FolderManager()

    def get_status(self, date_end=None):
        if not date_end:
            date_end = date.today()
        # filter in python manually because we cached things using prefetch_related
        actions_model_done = {
            action.model.pk
            for action in self.actions.all()
            if action.done and action.date <= date_end
        }
        all_statuses = list(self.model.statuses.all())
        statuses = [
            status
            for status in all_statuses
            if actions_model_done.intersection(
                {
                    action_model["pk"]
                    for action_model in status.action_models.all().values("pk")
                }
            )
        ]

        if statuses:
            return statuses[-1]
        else:
            if all_statuses:
                return all_statuses[0]

        return None

    def get_duration(self):
        if not self.model.project.custom_display_fields.get("duration"):
            return None
        duration = 0
        for action in self.actions.all():
            duration += action.duration
        return duration

    def __str__(self):
        return f"{self.model.name} - {self.pk}"

    def save(self, *args, **kwargs):
        self.type_valorization = (
            TypeValorization.objects.filter(groups=self.owning_group)
            .intersection(self.model.project.type_valorizations.all())
            .first()
        )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Dossier")
        verbose_name_plural = _("Dossiers")
