from core.models import MixeurBaseModel

from django.db import models
from django.utils.translation import ugettext_lazy as _


class ObjectiveStatusQueryset(models.QuerySet):
    def accessible_by(self, user):
        if user.is_administrator:
            return self

        groups = [user.group] + list(user.group.laureate_groups.all())
        return self.filter(group__in=groups)


class ObjectiveStatusManager(models.Manager.from_queryset(ObjectiveStatusQueryset)):
    pass


class ObjectiveStatus(MixeurBaseModel):
    name = models.CharField(verbose_name=_("Nom"), max_length=255)
    period = models.ForeignKey(
        "fac.Period",
        on_delete=models.CASCADE,
        related_name="objective_statuses",
        verbose_name="Période",
    )
    group = models.ForeignKey(
        "accounts.Group", related_name="objectifs", on_delete=models.CASCADE
    )
    status = models.ForeignKey(
        "Status", on_delete=models.CASCADE, related_name="objectives"
    )
    nb_statuses = models.PositiveIntegerField(verbose_name=_("Nombre de status requis"))
    objects = ObjectiveStatusManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Objectif")
        verbose_name_plural = _("Objectifs")
