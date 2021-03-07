from core.models import MixeurBaseModel

from django.db import models
from django.utils.translation import ugettext_lazy as _


class ObjectiveActionQueryset(models.QuerySet):
    def accessible_by(self, user):
        if user.is_administrator:
            return self

        groups = [user.group] + list(user.group.laureate_groups.all())
        return self.filter(group__in=groups)


class ObjectiveActionManager(models.Manager.from_queryset(ObjectiveActionQueryset)):
    pass


class ObjectiveAction(MixeurBaseModel):
    name = models.CharField(verbose_name=_("Nom"), max_length=255)
    period = models.ForeignKey(
        "fac.Period",
        on_delete=models.CASCADE,
        related_name="objective_actions",
        verbose_name="Période",
    )
    group = models.ForeignKey(
        "accounts.Group", related_name="objectif_actions", on_delete=models.CASCADE
    )
    model_action = models.ForeignKey(
        "ActionModel", on_delete=models.CASCADE, related_name="objectives"
    )
    nb_actions = models.PositiveIntegerField(
        verbose_name=_("Nombre d'actions requises")
    )
    objects = ObjectiveActionManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Objectif d'action")
        verbose_name_plural = _("Objectifs d'action")
