from core.models import MixeurBaseModel

from django.db import models
from django.utils.translation import ugettext_lazy as _


class BudgetQueryset(models.QuerySet):
    def accessible_by(self, user):
        if user.is_administrator:
            return self

        groups = [user.group] + list(user.group.laureate_groups.all())
        return self.filter(group__in=groups)


class BudgetManager(models.Manager.from_queryset(BudgetQueryset)):
    pass


class Budget(MixeurBaseModel):
    period = models.ForeignKey(
        "fac.Period", related_name="period_budgets", on_delete=models.CASCADE
    )
    total_envelope = models.PositiveIntegerField()
    group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe propriétaire"),
        on_delete=models.CASCADE,
        related_name="group_budgets",
    )
    project = models.ForeignKey(
        "fac.Project",
        verbose_name=_("Projet lié"),
        on_delete=models.CASCADE,
        related_name="project_budgets",
    )

    objects = BudgetManager()

    def budget_summary(self, graph_start, graph_end, graph_data, all_actions):
        """
        Returns the total expenses linked to this budget
        + increment the expenses present in `graph_data`
        :graph_start: The start of the query
        :graph_end: The end of the query
        :graph_data:
            A list of point with
                - a "date" key, representing the date at which the value is taken
                - a "cumulated_expenses", representing the amount of expenses at
                  this date
        :all_actions: all the done actions in the project, need to be filtered out
        :return:
        """

        start = max(self.period.date_start, graph_start)
        end = min(self.period.date_end, graph_end)

        # Get all actions done related to the project
        # Prefetch for performances
        actions_in_period = [
            action
            for action in all_actions
            if action.folder.owning_group == self.group
            and self.period.date_start <= action.date <= end
        ]

        total_expenses = 0

        for action in actions_in_period:
            action_cost = action.cost
            total_expenses += action_cost
            for graph_point in graph_data:
                if action.date <= graph_point["date"]:
                    graph_point["cumulated_expenses"] += action_cost

        return {
            "total_envelope": self.total_envelope,
            "total_expenses": total_expenses,
            "expenses_in_selected_time_lapse": total_expenses
            - sum(action.cost for action in actions_in_period if action.date < start),
            "period_start": start,
            "period_end": end,
        }

    def __str__(self):
        return f"Budget pour {self.period}"

    class Meta:
        verbose_name = _("Budget")
        verbose_name_plural = _("Budgets")
