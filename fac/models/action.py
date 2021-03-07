from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from core.models import MixeurBaseModel

from .tag import Tag


class ActionQueryset(models.QuerySet):
    def accessible_by(self, user):
        if user.is_administrator:
            return self

        return self.filter(folder__owning_group=user.group)


class ActionManager(models.Manager.from_queryset(ActionQueryset)):
    pass


class Action(MixeurBaseModel):

    objects = ActionManager()

    duration = models.DecimalField(
        verbose_name=_("Durée de la tâche en heure"),
        default=0,
        blank=True,
        max_digits=10,
        decimal_places=4,
    )
    date = models.DateField(null=True, blank=True)
    done = models.BooleanField(default=False, verbose_name=_("Réalisé"))
    done_by = models.ForeignKey(
        "accounts.User",
        related_name="actions_done",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        limit_choices_to=Q(user_type="advisor") | Q(user_type="superadvisor"),
    )
    message = models.TextField(verbose_name=_("Message"), default="", blank=True)
    folder = models.ForeignKey(
        "fac.Folder", on_delete=models.CASCADE, related_name="actions"
    )
    model = models.ForeignKey(
        "fac.ActionModel", on_delete=models.CASCADE, related_name="actions"
    )
    contact = models.ForeignKey(
        "fac.Contact",
        verbose_name=_("Contact"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    valorization = models.ForeignKey(
        "fac.Valorization",
        on_delete=models.SET_NULL,
        related_name="actions",
        null=True,
        blank=True,
    )
    reminder = GenericRelation(
        "fac.Reminder",
        related_query_name="action",
        content_type_field="content_type_task",
        object_id_field="object_id_task",
    )
    files = GenericRelation(
        "fac.File",
        related_query_name="action",
        content_type_field="content_type",
        object_id_field="object_id",
    )

    tags = models.ManyToManyField(
        to=Tag,
        related_name="linked_actions",
        verbose_name=_("Tags"),
        help_text=_("Liste de tags"),
        blank=True,
    )

    custom_form_data = JSONField(blank=True, null=True)

    @cached_property
    def owning_group(self):
        return self.folder.owning_group

    @cached_property
    def linked_object(self):
        return self.folder.linked_object

    @property
    def cost(self):
        if not self.done:
            return 0

        valorization = self.model.valorizations.filter(
            type_valorization__folders=self.folder,
            period__date_start__lte=self.date,
            period__date_end__gte=self.date,
        )

        if not valorization.exists():
            return 0
        valorization = valorization.first()

        valorization_amount = valorization.amount
        if self.model.coefficient_enabled:
            valorization_amount = valorization_amount * self.owning_group.coefficient
        if valorization.act:
            return float(valorization_amount)
        return float(valorization_amount * self.duration)

    @property
    def unit_valorization(self):
        if not self.valorization:
            return 0
        if self.model.coefficient_enabled:
            return float(self.valorization.amount * self.owning_group.coefficient)
        return float(self.valorization.amount)

    @property
    def quantity(self):
        if not self.valorization:
            return 1
        if self.valorization.act:
            return 1
        return float(self.duration)

    def is_act(self):
        if not self.valorization:
            return None
        return self.valorization.act

    def __str__(self):
        return self.model.name
