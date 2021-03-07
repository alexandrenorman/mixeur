# -*- coding: utf-8 -*-

# https://django-test-plus.readthedocs.io/en/latest/
from test_plus.test import TestCase

# from test_plus import APITestCase

from .factories import (
    ClientProfileFactory,
    AdvisorProfileFactory,
    ManagerProfileFactory,
    AdministratorProfileFactory,
    AdminGroupFactory,
    GroupFactory,
)
from visit_report.tests.factories import HousingFactory
from helpers.tests.tests_helpers import (
    UserAsAdministrator,
    ApiTestCase,
    UserAsManager,
    UserAsAdvisor,
    UserAsClient,
)


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client_user = ClientProfileFactory()
        self.group = GroupFactory(is_active=True)
        self.advisor = AdvisorProfileFactory(group=self.group, is_active=True)
        self.manager = ManagerProfileFactory(group=self.group, is_active=True)
        self.administrator = AdministratorProfileFactory(
            group=self.group, is_active=True
        )

    def test_login_with_wrong_password(self):
        import environ

        env = environ.Env()
        DEBUG = env.bool("DJANGO_DEBUG", default=False)

        if not DEBUG:
            response = self.post(
                "/api/v1/auth/obtain_token/",
                data={"email": self.client_user.email, "password": "TOTONOPASS"},
                format="json",
            )
            self.response_400(response)
            self.assertTrue("non_field_errors" in response.data)
        else:
            print("test_login_with_wrong_password not passed due to debug mode")

    def test_login_client(self):
        self.client_user.set_password("TOTO")
        self.client_user.save()
        self.assertTrue(self.client_user.check_password("TOTO"))
        response = self.post(
            "/api/v1/auth/obtain_token/",
            data={"email": self.client_user.email, "password": "TOTO"},
            format="json",
        )
        self.response_200(response)
        self.assertTrue("token" in response.data)

    def test_inactive_client_cannot_login(self):
        self.client_user.is_active = False
        self.client_user.save()
        response = self.post(
            "/api/v1/auth/obtain_token/",
            data={"email": self.client_user.email, "password": "TOTO"},
            format="json",
        )
        self.response_400(response)

    def test_login_advisor(self):
        self.advisor.set_password("TOTO")
        self.advisor.save()
        self.assertTrue(self.advisor.check_password("TOTO"))
        response = self.post(
            "/api/v1/auth/obtain_token/",
            data={"email": self.advisor.email, "password": "TOTO"},
        )
        self.response_200(response)
        self.assertTrue("token" in response.data)

    def test_login_manager(self):
        self.manager.set_password("TOTO")
        self.manager.save()
        self.assertTrue(self.manager.check_password("TOTO"))
        response = self.post(
            "/api/v1/auth/obtain_token/",
            data={"email": self.manager.email, "password": "TOTO"},
        )
        self.response_200(response)
        self.assertTrue("token" in response.data)

    def test_login_administrator(self):
        self.administrator.set_password("TOTO")
        self.administrator.save()
        self.assertTrue(self.administrator.check_password("TOTO"))
        response = self.post(
            "/api/v1/auth/obtain_token/",
            data={"email": self.administrator.email, "password": "TOTO"},
        )
        self.response_200(response)
        self.assertTrue("token" in response.data)


class GroupViewTestCase(ApiTestCase):
    def setUp(self):
        super().setUp()

        self.admin_group = AdminGroupFactory()
        self.group = GroupFactory(admin_group=self.admin_group)
        self.other_admin_group = AdminGroupFactory()
        self.other_group = GroupFactory(admin_group=self.other_admin_group)

        self.manager = ManagerProfileFactory(group=self.admin_group)

        self.advisor = AdvisorProfileFactory(group=self.group)
        self.other_advisor = AdvisorProfileFactory(group=self.other_group)

        self.manager.set_password("password")
        self.manager.save()

        self.advisor.set_password("password")
        self.advisor.save()
        self.other_advisor.set_password("password")
        self.other_advisor.save()

    def test_administrator_view(self):
        with UserAsAdministrator(self):
            response = self.get(f"/api/v1/accounts/group/{self.group.pk}/")

        self.response_200(response)
        # data = json.loads(response.content)

    def test_manager_view(self):
        with UserAsManager(self, self.manager):
            response = self.get(f"/api/v1/accounts/group/{self.group.pk}/")
            self.response_200(response)
            # data = json.loads(response.content)

            response = self.get(f"/api/v1/accounts/group/{self.other_group.pk}/")
            self.response_200(response)
        # data = json.loads(response.content)

    def test_advisor_view(self):
        with UserAsAdvisor(self, self.advisor):
            response = self.get(f"/api/v1/accounts/group/{self.group.pk}/")

        self.response_200(response)
        # data = json.loads(response.content)

    def test_other_advisor_view(self):
        with UserAsAdvisor(self, self.other_advisor):
            response = self.get(f"/api/v1/accounts/group/{self.group.pk}/")

        self.response_200(response)
        # data = json.loads(response.content)

    def test_client_view(self):
        with UserAsClient(self):
            response = self.get(f"/api/v1/accounts/group/{self.group.pk}/")

        self.response_403(response)
        # data = json.loads(response.content)


class UserViewTestCase(ApiTestCase):
    def setUp(self):
        super().setUp()

        self.client_profile = ClientProfileFactory()
        self.housing = HousingFactory(user=self.client_profile)

    def test_anonymous_cant_access(self):
        first_name = self.client_profile.first_name
        response = self.get("profile:user_list", data={"q": first_name})
        self.response_403(response)

    def test_search_user_view(self):
        first_name = self.client_profile.first_name

        with UserAsAdministrator(self):
            response = self.get("profile:user_list", data={"q": first_name})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        values = response.json()[0]
        self.assertEqual(values["last_name"], self.client_profile.last_name)

    def test_search_user_by_profile_type_view(self):
        first_name = self.client_profile.first_name
        profile_type = self.client_profile.user_type
        with UserAsAdministrator(self):
            response = self.get(
                "/api/v1/accounts/user/", data={"q": first_name, "type": profile_type}
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        values = response.json()[0]
        self.assertEqual(values["last_name"], self.client_profile.last_name)

    def test_search_by_housing_address_view(self):
        partial_address = self.housing.city
        self.assertIn(partial_address, self.housing.address)

        with UserAsAdministrator(self):
            response = self.get("/api/v1/accounts/user/", data={"q": partial_address})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        values = response.json()[0]
        self.assertEqual(values["last_name"], self.client_profile.last_name)

    def test_search_on_phone_number(self):
        phone = str(self.client_profile.phone).replace("+33", "0")
        with UserAsAdministrator(self):
            response = self.get("/api/v1/accounts/user/", data={"q": phone})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        values = response.json()[0]
        self.assertEqual(values["last_name"], self.client_profile.last_name)
