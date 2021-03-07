from decimal import Decimal
from django.test import TestCase

from .factories import BudgetFactory

from .test_fap import InitFapModelMixin


class CoefficientTestCase(InitFapModelMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.user_group.coefficient = Decimal("0.65")
        self.user_group.save()

        BudgetFactory(group=self.user_group, project=self.project, period=self.period)

        self.valorization_1.act = False
        self.valorization_1.save()

        self.action_1.valorization = self.valorization_1
        self.action_2.valorization = self.valorization_1

        self.action_1.done = True
        self.action_2.done = True

        self.action_1.date = self.period.date_start
        self.action_2.date = self.period.date_start

        # Coefficient apply just on action_2
        self.action_2.model.coefficient_enabled = True

        self.action_1.save()
        self.action_2.save()

    def test_without_coefficient_enabled_duration(self):
        self.assertEquals(self.action_1.valorization.act, False)
        self.assertNotEquals(self.action_1.owning_group.coefficient, 1)
        self.assertEquals(
            self.action_1.cost,
            float((self.action_1.valorization.amount) * self.action_1.duration),
        )

    def test_coefficient_act(self):
        self.valorization_1.act = True
        self.valorization_1.save()
        self.assertEquals(self.action_2.valorization.act, True)
        self.assertEquals(
            self.action_2.cost,
            float(self.valorization_1.amount * self.user_group.coefficient),
        )
