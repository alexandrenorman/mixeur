# -*- coding: utf-8 -*-

# https://django-test-plus.readthedocs.io/en/latest/
from test_plus.test import TestCase
from abc import ABC, abstractmethod

from helpers.helpers import unique_filename_in_path
from accounts.tests.factories import (
    ClientProfileFactory,
    AdvisorProfileFactory,
    ManagerProfileFactory,
    AdministratorProfileFactory,
)


class UniqueFilenameTestCase(TestCase):
    def test_no_file(self):
        self.assertEquals(
            unique_filename_in_path("/", "file-do-not-exist-on-disk.txt"),
            "file-do-not-exist-on-disk.txt",
        )

    def test_when_file_exists(self):
        self.assertEquals(
            unique_filename_in_path("/etc/", "resolv.conf"), "resolv-1.conf"
        )


class ApiTestCase(TestCase):
    """
    Helper for using TestCase for API's test

    Create default users on setup : api_administrator, api_manager, api_advisor and api_client
    """

    def setUp(self):
        self.api_administrator = AdministratorProfileFactory()
        self.api_administrator.set_password("password")
        self.api_administrator.save()

        self.api_manager = ManagerProfileFactory()
        self.api_manager.set_password("password")
        self.api_manager.save()

        self.api_advisor = AdvisorProfileFactory()
        self.api_advisor.set_password("password")
        self.api_advisor.save()

        self.api_client = ClientProfileFactory()
        self.api_client.set_password("password")
        self.api_client.save()


class AsLogin(ABC):
    """
    Abstract context manager which logins as administrator in a TestCase context

    Usage:
    with UserAsAdministrator(self):
        response = self.get("profile:user_list", data={"q": first_name})

    """

    def __init__(self, testcase: ApiTestCase, user=None) -> None:
        self.testcase = testcase
        self.user = user

    def __enter__(self):
        if self.user:
            return self.testcase.login(email=self.user.email, password="password")
        else:
            return self.testcase.login(email=self._get_email(), password="password")

    def __exit__(self, type, value, traceback) -> None:
        return

    @abstractmethod
    def _get_email(self):
        raise ValueError


class UserAsAdministrator(AsLogin):
    """
    Context manager which logins as administrator in a TestCase context

    Usage:
    with UserAsAdministrator(self):
        response = self.get("profile:user_list", data={"q": first_name})

    """

    def _get_email(self):
        return self.testcase.api_administrator.email


class UserAsManager(AsLogin):
    """
    Context manager which logins as manager in a TestCase context

    Usage:
    with UserAsManager(self):
        response = self.get("profile:user_list", data={"q": first_name})

    """

    def _get_email(self):
        return self.testcase.api_manager.email


class UserAsAdvisor(AsLogin):
    """
    Context advisor which logins as advisor in a TestCase context

    Usage:
    with UserAsAdvisor(self):
        response = self.get("profile:user_list", data={"q": first_name})

    """

    def _get_email(self):
        return self.testcase.api_advisor.email


class UserAsClient(AsLogin):
    """
    Context client which logins as client in a TestCase context

    Usage:
    with UserAsClient(self):
        response = self.get("profile:user_list", data={"q": first_name})

    """

    def _get_email(self):
        return self.testcase.api_client.email
