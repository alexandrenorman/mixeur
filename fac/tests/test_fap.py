from datetime import date, timedelta

from dateutil.relativedelta import relativedelta

from django.test import Client, TestCase
from django.urls import reverse

from accounts.tests import AdminGroupFactory, GroupFactory, UserFactory

from fac.models import Project

from .factories import (
    ActionFactory,
    ActionModelFactory,
    BudgetFactory,
    CategoryModelFactory,
    ContactFactory,
    FolderFactory,
    FolderModelFactory,
    ObjectiveStatusFactory,
    PeriodFactory,
    ProjectFactory,
    StatusFactory,
    TypeValorizationFactory,
    ValorizationFactory,
)
from ..models import Action, Folder


class InitFapModelMixin:
    def setUp(self):  # NOQA: CFQ001
        self.anonymous_client = Client()
        self.advisor_client = Client()
        self.user_group = GroupFactory()
        self.admin_group = AdminGroupFactory()
        self.contact = ContactFactory(owning_group=self.user_group)
        self.advisor = UserFactory(user_type="advisor", group=self.user_group)
        self.admin_client = Client()
        self.admin = UserFactory(
            user_type="administrator",
            group=self.admin_group,
            is_staff=True,
            is_superuser=True,
        )
        assert self.admin_client.login(username=self.admin.email, password="password")
        assert self.advisor_client.login(
            username=self.advisor.email, password="password"
        )
        self.start_period = date.today()  # date(year=2019, month=1, day=1)
        self.end_period = date.today() + relativedelta(
            months=3
        )  # date(year=2019, month=3, day=31)
        self.period = PeriodFactory(
            name="2019", date_start=self.start_period, date_end=self.end_period
        )

        self.group_2 = GroupFactory()
        self.group_3 = GroupFactory()
        self.type_valorization_1 = TypeValorizationFactory(groups=[self.user_group])
        self.type_valorization_2 = TypeValorizationFactory(groups=[self.group_2])
        self.type_valorization_3 = TypeValorizationFactory(groups=[self.group_3])
        self.valorization_1 = ValorizationFactory(
            type_valorization=self.type_valorization_1, period=self.period
        )
        self.valorization_2 = ValorizationFactory(
            type_valorization=self.type_valorization_2, period=self.period
        )
        self.valorization_3 = ValorizationFactory(
            type_valorization=self.type_valorization_3, period=self.period
        )
        self.project = ProjectFactory(
            type_valorizations=(
                self.type_valorization_1,
                self.type_valorization_2,
                self.type_valorization_3,
            ),
            groups=(self.user_group, self.group_2, self.group_3),
        )
        self.budget = BudgetFactory(
            period=self.period, group=self.user_group, project=self.project
        )
        self.folder_model = FolderModelFactory(project=self.project)
        self.category_model = CategoryModelFactory(folder_model=self.folder_model)
        self.status_1 = StatusFactory(order=1, folder_model=self.folder_model)
        self.status_2 = StatusFactory(order=3, folder_model=self.folder_model)
        self.status_3 = StatusFactory(order=2, folder_model=self.folder_model)
        self.action_model_1 = ActionModelFactory(
            category_model=self.category_model,
            default=True,
            trigger_status=self.status_1,
            order=1,
            valorizations=(
                self.valorization_1,
                self.valorization_2,
                self.valorization_3,
            ),
        )
        self.action_model_2 = ActionModelFactory(
            category_model=self.category_model,
            default=True,
            trigger_status=self.status_2,
            order=2,
            valorizations=(
                self.valorization_1,
                self.valorization_2,
                self.valorization_3,
            ),
        )
        self.action_model_3 = ActionModelFactory(
            category_model=self.category_model,
            optional=True,
            trigger_status=self.status_3,
            order=3,
            valorizations=(
                self.valorization_1,
                self.valorization_2,
                self.valorization_3,
            ),
        )
        self.action_model_4 = ActionModelFactory(
            category_model=self.category_model,
            default=True,
            order=4,
            trigger_status=self.status_2,
            valorizations=(),
        )
        self.folder = FolderFactory(
            owning_group=self.user_group,
            model=self.folder_model,
            linked_object=self.contact,
        )
        # get the folder's status once, so that it's cached
        assert self.folder.get_status(date.today()) == self.status_1
        self.action_1 = ActionFactory(
            folder=self.folder,
            model=self.action_model_1,
            valorization=self.valorization_1,
        )
        self.action_2 = ActionFactory(
            folder=self.folder,
            model=self.action_model_2,
            valorization=self.valorization_1,
        )
        self.action_3 = ActionFactory(
            folder=self.folder,
            model=self.action_model_3,
            valorization=self.valorization_1,
        )

        self.objective_1 = ObjectiveStatusFactory(
            period=self.period,
            group=self.user_group,
            status=self.status_1,
            nb_statuses=10,
        )


class FolderTestCase(InitFapModelMixin, TestCase):
    def test_folder_view_403(self):
        response = self.anonymous_client.get(reverse("fac:folder_list"))
        self.assertEqual(response.status_code, 403)

    def test_folder_view_list_no_group(self):
        response = self.advisor_client.get(
            reverse("fac:folder_list")
            + f"?objectId={self.contact.pk}&linkedObjectType=contact"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_folder_view_list(self):
        response = self.advisor_client.get(
            reverse("fac:folder_list")
            + f"?objectId={self.contact.pk}&linkedObjectType=contact"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_folder_view_list_no_linked_object_type(self):
        response = self.advisor_client.get(
            reverse("fac:folder_list") + f"?objectId={self.contact.pk}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_folder_view_list_no_object_id(self):
        response = self.advisor_client.get(
            reverse("fac:folder_list") + "?linkedObjectType=contact"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)


class StatusTestCase(InitFapModelMixin, TestCase):
    def test_status_folder(self):
        folder = Folder.objects.first()
        self.assertEquals(self.status_1.pk, folder.get_status().pk)

    def test_status_no_action(self):
        self.assertEquals(
            self.status_1.pk,
            FolderFactory(model=self.folder_model, owning_group=self.user_group)
            .get_status()
            .pk,
        )

    def test_status_no_action_done(self):
        folder = FolderFactory(model=self.folder_model, owning_group=self.user_group)
        ActionFactory(
            folder=folder,
            done=False,
            model=self.action_model_1,
            valorization=self.valorization_1,
        )
        self.assertEquals(self.status_1.pk, folder.get_status().pk)


class AdminProjectTestCase(InitFapModelMixin, TestCase):
    def test_valorizations_fill_project_groups(self):
        self.assertEquals(Project.objects.count(), 2)
        response = self.admin_client.post(
            reverse("admin:fac_project_add"),
            data={
                "name": "Testimo",
                "type_valorizations": [self.type_valorization_1.pk],
                "budget": self.budget.pk,
            },
        )
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Project.objects.count(), 3)
        created_project = Project.objects.filter(name="Testimo").first()
        self.assertEquals(
            created_project.groups.first().pk,
            self.type_valorization_1.groups.first().pk,
        )

    def test_rule_group_type_valorization_project(self):
        self.assertEquals(Project.objects.count(), 2)
        self.type_valorization_4 = TypeValorizationFactory(groups=[self.user_group])

        # This replaces the old test
        # as when raising an Exception in ProjectAdminForm.clean_type_valorizations
        # seems not to be handle in django 2.2
        # In Dj 3, we could use raise_request_exception=False
        with self.assertRaises(TypeError) as context:
            self.admin_client.post(
                reverse("admin:fac_project_add"),
                data={
                    "name": "Testimo",
                    "type_valorizations": [
                        self.type_valorization_1.pk,
                        self.type_valorization_4.pk,
                    ],
                    "budget": self.budget.pk,
                },
            )
        self.assertEquals(
            "the JSON object must be str, bytes or bytearray, not 'NoneType'",
            str(context.exception),
        )

        # >>> response = self.admin_client.post(
        # >>>     reverse("admin:fac_project_add"),
        # >>>     data={
        # >>>         "name": "Testimo",
        # >>>         "type_valorizations": [
        # >>>             self.type_valorization_1.pk,
        # >>>             self.type_valorization_4.pk,
        # >>>         ],
        # >>>             "budget": self.budget.pk,
        # >>>     },
        # >>> )
        # >>> self.assertEquals(Project.objects.count(), 2)
        # >>> self.assertEquals(response.status_code, 200)
        # >>> self.assertEquals(
        # >>>     response.context_data["errors"][0][0],
        # >>>     (
        # >>>         "Vous ne pouvez pas associer plusieurs types de valorisation "
        # >>>         "appartenant au même groupe."
        # >>>     ),
        # >>> )

    def test_rule_group_type_valorization_folder_model_done(self):
        self.assertEquals(Project.objects.count(), 2)
        response = self.admin_client.post(
            reverse("admin:fac_project_add"),
            data={
                "name": "Testimo",
                "type_valorizations": [
                    self.type_valorization_1.pk,
                    self.type_valorization_2.pk,
                ],
                "budget": self.budget.pk,
            },
        )
        self.assertEquals(Project.objects.count(), 3)
        self.assertEquals(response.status_code, 302)

    def test_add_group_on_type_valorization(self):
        self.type_valorization_1.groups.remove(self.user_group)
        self.project.groups.remove(self.user_group)
        actual_groups = {group.pk for group in self.project.groups.all()}
        expected_groups = {
            group.pk
            for type_valorization in self.project.type_valorizations.all()
            for group in type_valorization.groups.all()
        }
        self.assertEquals(expected_groups, actual_groups)
        self.admin_client.post(
            reverse(
                "admin:fac_typevalorization_change", args=(self.type_valorization_1.pk,)
            ),
            data={
                "name": self.type_valorization_1.name,
                "groups": [group.pk for group in self.type_valorization_1.groups.all()]
                + [self.user_group.pk],
            },
        )
        actual_groups_2 = {group.pk for group in self.project.groups.all()}
        expected_groups_2 = {
            group.pk
            for type_valorization in self.project.type_valorizations.all()
            for group in type_valorization.groups.all()
        }
        self.assertEquals(expected_groups_2, actual_groups_2)
        self.assertNotEquals(actual_groups_2, actual_groups)


class ActionTestCase(InitFapModelMixin, TestCase):
    def test_action_view(self):
        response = self.anonymous_client.get(reverse("fac:action_list"))
        self.assertEqual(response.status_code, 403)

    def test_action_create(self):
        response = self.advisor_client.post(
            reverse("fac:action_list"),
            data={
                "duration": 360,
                "done": True,
                "message": "Mon message",
                "folder": self.folder.pk,
                "model": self.action_model_1.pk,
                "reminder": {
                    "date": "2020-05-08",
                    "persons": [{"value": self.advisor.pk, "label": str(self.advisor)}],
                },
            },
            format="json",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        action = Action.objects.get(pk=response.json().get("pk"))
        self.assertEqual(action.folder, self.folder)
        self.assertEqual(action.model, self.action_model_1)
        self.assertEqual(action.done, True)
        self.assertEqual(action.done_by, self.advisor)
        self.assertEqual(action.valorization, self.valorization_1)

    def test_action_undone(self):
        action = ActionFactory(
            folder=self.folder,
            model=self.action_model_1,
            done_by=self.advisor,
            done=True,
        )

        response = self.advisor_client.patch(
            reverse("fac:action_detail", kwargs={"pk": action.pk}),
            data={
                "done": False,
                "folder": action.folder.pk,
                "model": action.model.pk,
                "pk": action.pk,
                "reminder": {
                    "date": "2020-05-08",
                    "persons": [{"value": self.advisor.pk, "label": str(self.advisor)}],
                },
            },
            format="json",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        action.refresh_from_db()
        self.assertEqual(action.done, False)
        self.assertEqual(action.done_by, None)

    def test_action_update_by_another(self):
        action = ActionFactory(
            folder=self.folder,
            model=self.action_model_1,
            done_by=self.advisor,
            done=True,
        )

        advisor_client2 = Client()
        advisor2 = UserFactory(user_type="advisor", group=self.user_group)
        advisor_client2.login(username=advisor2.email, password="password")

        response = advisor_client2.patch(
            reverse("fac:action_detail", kwargs={"pk": action.pk}),
            data={
                "folder": action.folder.pk,
                "model": action.model.pk,
                "pk": action.pk,
                "done": True,
                "done_by": self.advisor.pk,
                "reminder": {
                    "date": "2020-05-08",
                    "persons": [{"value": self.advisor.pk, "label": str(self.advisor)}],
                },
            },
            format="json",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        action.refresh_from_db()
        self.assertEqual(action.done, True)
        self.assertEqual(action.done_by, self.advisor)

    def test_action_without_valorization(self):
        # action_model_4 have not period
        response = self.advisor_client.post(
            reverse("fac:action_list"),
            data={
                "duration": 360,
                "done": True,
                "message": "Mon message",
                "folder": self.folder.pk,
                "model": self.action_model_4.pk,
                "reminder": {
                    "date": "2020-05-08",
                    "persons": [{"value": self.advisor.pk, "label": str(self.advisor)}],
                },
            },
            format="json",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        action = Action.objects.get(pk=response.json().get("pk"))
        self.assertEqual(action.folder, self.folder)
        self.assertEqual(action.model, self.action_model_4)
        self.assertEqual(action.done, True)
        self.assertEqual(action.done_by, self.advisor)
        self.assertEqual(action.valorization, None)

    def test_action_valorization_out_period(self):
        yesterday = date.today() - timedelta(1)
        outdated_period = PeriodFactory(
            name="2019", date_start=yesterday, date_end=yesterday
        )

        outdated_valorization = ValorizationFactory(
            type_valorization=self.type_valorization_1, period=outdated_period
        )

        action_model_with_outdated_valorisation = ActionModelFactory(
            category_model=self.category_model,
            default=True,
            trigger_status=self.status_2,
            valorizations=(outdated_valorization,),
        )

        outdated_project = ProjectFactory(type_valorizations=[self.type_valorization_1])
        outdated_folder_model = FolderModelFactory(project=outdated_project)

        outdated_folder = FolderFactory(
            owning_group=self.user_group,
            model=outdated_folder_model,
            linked_object=self.contact,
        )

        response = self.advisor_client.post(
            reverse("fac:action_list"),
            data={
                "duration": 360,
                "done": True,
                "message": "Mon message",
                "folder": outdated_folder.pk,
                "model": action_model_with_outdated_valorisation.pk,
                "reminder": {
                    "date": "2020-05-08",
                    "persons": [{"value": self.advisor.pk, "label": str(self.advisor)}],
                },
            },
            format="json",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        action = Action.objects.get(pk=response.json().get("pk"))
        self.assertEqual(action.folder, outdated_folder)
        self.assertEqual(action.model, action_model_with_outdated_valorisation)
        self.assertEqual(action.done, True)
        self.assertEqual(action.done_by, self.advisor)
        self.assertEqual(action.valorization, None)

    def test_action_delete_updates_folder_status(self):
        self.assertEquals(self.folder.get_status().pk, self.status_1.pk)
        action = ActionFactory(
            folder=self.folder,
            model=self.action_model_2,
            done_by=self.advisor,
            done=True,
        )
        self.folder.refresh_from_db()
        self.assertEquals(self.folder.get_status().pk, self.status_2.pk)

        response = self.advisor_client.delete(
            reverse("fac:action_detail", kwargs={"pk": action.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["folder_status"]["name"], self.status_1.name)

        self.folder.refresh_from_db()
        self.assertEquals(self.folder.get_status().pk, self.status_1.pk)

    def test_cost_out_of_period(self):
        today = date.today()
        start = today - timedelta(days=3)
        end = today - timedelta(days=1)
        period = PeriodFactory(date_start=start, date_end=end)
        valorization = ValorizationFactory(act=True, amount=20, period=period)
        action = ActionFactory(
            duration=50,
            date=date.today(),
            done=True,
            valorization=valorization,
            folder=self.folder,
        )
        self.assertEquals(action.cost, 0)

    def test_cost_not_done(self):
        today = date.today()
        start = today - timedelta(days=3)
        end = today + timedelta(days=3)
        period = PeriodFactory(date_start=start, date_end=end)
        valorization = ValorizationFactory(act=True, amount=20, period=period)
        action = ActionFactory(
            duration=50,
            date=date.today(),
            done=False,
            valorization=valorization,
            folder=self.folder,
        )
        self.assertEquals(action.cost, 0)

    def test_cost_act(self):
        today = date.today()
        start = today - timedelta(days=3)
        end = today + timedelta(days=3)
        period = PeriodFactory(date_start=start, date_end=end)
        valorization = ValorizationFactory(act=True, amount=20, period=period)
        action = ActionFactory(
            duration=50,
            date=date.today(),
            done=True,
            valorization=valorization,
            folder=self.folder,
        )
        self.assertEquals(action.cost, 20)

    def test_cost_duration(self):
        today = date.today()
        start = today - timedelta(days=3)
        end = today + timedelta(days=3)
        period = PeriodFactory(date_start=start, date_end=end)
        valorization = ValorizationFactory(act=False, amount=20, period=period)
        action = ActionFactory(
            duration=50,
            date=date.today(),
            done=True,
            valorization=valorization,
            folder=self.folder,
        )
        self.assertEquals(action.cost, 1000)


class BudgetTestCase(InitFapModelMixin, TestCase):
    def test_budget_summary(self):
        start_summary_date = self.start_period + relativedelta(days=3)
        end_summary_date = self.end_period - timedelta(days=3)
        all_actions = []
        valorization = ValorizationFactory(
            act=True,
            amount=20,
            period=self.period,
            type_valorization=self.type_valorization_1,
        )
        action_model = ActionModelFactory(valorizations=[valorization])
        last_action = ActionFactory(
            duration=50,
            date=start_summary_date + relativedelta(days=1),
            done=True,
            valorization=valorization,
            folder=self.folder,
            model=action_model,
        )
        all_actions.append(last_action)
        # Not take in account, action done after end_summary_date
        all_actions.append(
            ActionFactory(
                duration=50,
                date=end_summary_date + relativedelta(days=1),
                done=True,
                valorization=valorization,
                folder=self.folder,
                model=action_model,
            )
        )
        # Not take in account, action done before start_summary_date
        all_actions.append(
            ActionFactory(
                duration=50,
                date=start_summary_date - relativedelta(days=1),
                done=True,
                valorization=valorization,
                folder=self.folder,
                model=action_model,
            )
        )
        self.maxDiff = None
        graph_data = [
            {"date": start_summary_date, "cumulated_expenses": 0.0},
            {"date": last_action.date, "cumulated_expenses": 0.0},
        ]
        budget = self.budget.budget_summary(
            graph_start=start_summary_date,
            graph_end=end_summary_date,
            graph_data=graph_data,
            all_actions=all_actions,
        )
        self.assertEquals(
            graph_data[0], {"date": start_summary_date, "cumulated_expenses": 20.0}
        )
        self.assertEquals(
            graph_data[1], {"date": last_action.date, "cumulated_expenses": 40.0}
        )
        self.assertEquals(budget["total_envelope"], self.budget.total_envelope)
        self.assertEquals(budget["total_expenses"], 40.0)
        self.assertEquals(budget["expenses_in_selected_time_lapse"], 20.0)
        self.assertEquals(budget["period_start"], start_summary_date)
        self.assertEquals(budget["period_end"], end_summary_date)
