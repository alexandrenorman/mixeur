# -*- coding: utf-8 -*-

# https://django-test-plus.readthedocs.io/en/latest/
from test_plus.test import TestCase

from .factories import (
    ClientProfileFactory,
    AdvisorProfileFactory,
    SuperAdvisorProfileFactory,
    ManagerProfileFactory,
    AdministratorProfileFactory,
    GroupFactory,
    AdminGroupFactory,
)

from simple_perms.helpers import AssertPermissions


class UserPermTestCase(AssertPermissions, TestCase):
    def setUp(self):
        self.client = ClientProfileFactory()

        self.admin_group = AdminGroupFactory()
        self.other_admin_group = AdminGroupFactory()

        self.group = GroupFactory(admin_group=self.admin_group)
        self.other_group = GroupFactory(admin_group=self.other_admin_group)

        self.advisor = AdvisorProfileFactory(group=self.group)
        self.superadvisor = SuperAdvisorProfileFactory(group=self.group)
        self.manager = ManagerProfileFactory(group=self.admin_group)
        self.administrator = AdministratorProfileFactory(group=self.group)

        self.other_advisor = AdvisorProfileFactory(group=self.other_group)
        self.other_manager = ManagerProfileFactory(group=self.other_admin_group)
        self.other_administrator = AdministratorProfileFactory(group=self.other_group)

    def test_client_perms(self):
        # fmt: off
        permissions = [
            {'usr': 'client', 'perm': 'user.view',   'args': (self.client, ),        'result': True},   # NOQA: E501,E241
            {'usr': 'client', 'perm': 'user.view',   'args': (self.advisor, ),       'result': False},  # NOQA: E501,E241
            {'usr': 'client', 'perm': 'user.view',   'args': (self.manager, ),       'result': False},  # NOQA: E501,E241
            {'usr': 'client', 'perm': 'user.view',   'args': (self.administrator, ), 'result': False},  # NOQA: E501,E241
            {'usr': 'client', 'perm': 'user.change', 'args': (self.client, ),        'result': True},   # NOQA: E501,E241
            {'usr': 'client', 'perm': 'user.change', 'args': (self.advisor, ),       'result': False},  # NOQA: E501,E241
            {'usr': 'client', 'perm': 'user.change', 'args': (self.manager, ),       'result': False},  # NOQA: E501,E241
            {'usr': 'client', 'perm': 'user.change', 'args': (self.administrator, ), 'result': False},  # NOQA: E501,E241
            
            {
                'usr': 'client',
                'perm': 'user.change_user_type',
                'args': ({'user_modified': self.client, "to_user_type": "client"}, ),
                'result': False,
            },
            {
                'usr': 'client',
                'perm': 'user.change_user_type',
                'args': ({'user_modified': self.client, "to_user_type": "advisor"}, ),
                'result': False,
            },
            {
                'usr': 'client',
                'perm': 'user.change_user_type',
                'args': ({'user_modified': self.client, "to_user_type": "manager"}, ),
                'result': False,
            },
            {
                'usr': 'client',
                'perm': 'user.change_user_type',
                'args': ({'user_modified': self.client, "to_user_type": "administrator"}, ),
                'result': False,
            },
        ]
        # fmt: on
        self.assertPerms(permissions)

    def change_user_type_perm_generator(
        self,
        user,
        user_modified,
        for_client,
        for_advisor,
        for_superadvisor,
        for_manager,
        for_administrator,
    ):  # NOQA: E501
        return [
            {
                "usr": user,
                "perm": "user.change_user_type",
                "args": ({"user_modified": user_modified, "to_user_type": "client"},),
                "result": for_client,
            },
            {
                "usr": user,
                "perm": "user.change_user_type",
                "args": ({"user_modified": user_modified, "to_user_type": "advisor"},),
                "result": for_advisor,
            },
            {
                "usr": user,
                "perm": "user.change_user_type",
                "args": (
                    {"user_modified": user_modified, "to_user_type": "superadvisor"},
                ),
                "result": for_superadvisor,
            },
            {
                "usr": user,
                "perm": "user.change_user_type",
                "args": ({"user_modified": user_modified, "to_user_type": "manager"},),
                "result": for_manager,
            },
            {
                "usr": user,
                "perm": "user.change_user_type",
                "args": (
                    {"user_modified": user_modified, "to_user_type": "administrator"},
                ),
                "result": for_administrator,
            },
        ]

    def test_advisor_perms(self):
        # fmt: off
        permissions = [
            # View perm
            {'usr': 'advisor', 'perm': 'user.view',   'args': (self.client, ),              'result': True},   # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'user.view',   'args': (self.advisor, ),             'result': True},   # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'user.view',   'args': (self.manager, ),             'result': True},   # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'user.view',   'args': (self.administrator, ),       'result': True},   # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'user.view',   'args': (self.other_advisor, ),       'result': True},   # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'user.view',   'args': (self.other_manager, ),       'result': True},   # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'user.view',   'args': (self.other_administrator, ), 'result': True},   # NOQA: E501,E241
            
            # Change perm
            {'usr': 'advisor', 'perm': 'user.change', 'args': (self.client, ),              'result': True},   # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'user.change', 'args': (self.advisor, ),             'result': True},   # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'user.change', 'args': (self.manager, ),             'result': False},  # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'user.change', 'args': (self.administrator, ),       'result': False},  # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'user.change', 'args': (self.other_advisor, ),       'result': False},  # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'user.change', 'args': (self.other_manager, ),       'result': False},  # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'user.change', 'args': (self.other_administrator, ), 'result': False},  # NOQA: E501,E241

        ] + self.change_user_type_perm_generator(
            user='advisor',
            user_modified=self.client,
            for_client=False,
            for_advisor=False,
            for_superadvisor=False,
            for_manager=False,
            for_administrator=False,
        ) + self.change_user_type_perm_generator(
            user='advisor',
            user_modified=self.advisor,
            for_client=False,
            for_advisor=False,
            for_superadvisor=False,
            for_manager=False,
            for_administrator=False,
        ) + self.change_user_type_perm_generator(
            user='advisor',
            user_modified=self.superadvisor,
            for_client=False,
            for_advisor=False,
            for_superadvisor=False,
            for_manager=False,
            for_administrator=False,
        ) + self.change_user_type_perm_generator(
            user='advisor',
            user_modified=self.manager,
            for_client=False,
            for_advisor=False,
            for_superadvisor=False,
            for_manager=False,
            for_administrator=False,
        ) + self.change_user_type_perm_generator(
            user='advisor',
            user_modified=self.administrator,
            for_client=False,
            for_advisor=False,
            for_superadvisor=False,
            for_manager=False,
            for_administrator=False,
        )
        # fmt: on
        self.assertPerms(permissions)

    def test_superadvisor_perms(self):
        # fmt: off
        permissions = [
            # # View perm
            {'usr': 'superadvisor', 'perm': 'user.view',   'args': (self.client, ),              'result': True},   # NOQA: E501,E241
            {'usr': 'superadvisor', 'perm': 'user.view',   'args': (self.advisor, ),             'result': True},   # NOQA: E501,E241
            {'usr': 'superadvisor', 'perm': 'user.view',   'args': (self.manager, ),             'result': True},   # NOQA: E501,E241
            {'usr': 'superadvisor', 'perm': 'user.view',   'args': (self.administrator, ),       'result': True},   # NOQA: E501,E241
            {'usr': 'superadvisor', 'perm': 'user.view',   'args': (self.other_advisor, ),       'result': True},   # NOQA: E501,E241
            {'usr': 'superadvisor', 'perm': 'user.view',   'args': (self.other_manager, ),       'result': True},   # NOQA: E501,E241
            {'usr': 'superadvisor', 'perm': 'user.view',   'args': (self.other_administrator, ), 'result': True},   # NOQA: E501,E241

            # Change perm
            {'usr': 'superadvisor', 'perm': 'user.change', 'args': (self.client, ),              'result': True},   # NOQA: E501,E241
            {'usr': 'superadvisor', 'perm': 'user.change', 'args': (self.advisor, ),             'result': True},   # NOQA: E501,E241
            {'usr': 'superadvisor', 'perm': 'user.change', 'args': (self.manager, ),             'result': False},  # NOQA: E501,E241
            {'usr': 'superadvisor', 'perm': 'user.change', 'args': (self.administrator, ),       'result': False},  # NOQA: E501,E241
            {'usr': 'superadvisor', 'perm': 'user.change', 'args': (self.other_advisor, ),       'result': False},  # NOQA: E501,E241
            {'usr': 'superadvisor', 'perm': 'user.change', 'args': (self.other_manager, ),       'result': False},  # NOQA: E501,E241
            {'usr': 'superadvisor', 'perm': 'user.change', 'args': (self.other_administrator, ), 'result': False},  # NOQA: E501,E241

        ] + self.change_user_type_perm_generator(
            user='superadvisor',
            user_modified=self.client,
            for_client=False,
            for_advisor=False,
            for_superadvisor=False,
            for_manager=False,
            for_administrator=False,
        ) + self.change_user_type_perm_generator(
            user='superadvisor',
            user_modified=self.advisor,
            for_client=False,
            for_advisor=True,
            for_superadvisor=True,
            for_manager=False,
            for_administrator=False,
        ) + self.change_user_type_perm_generator(
            user='superadvisor',
            user_modified=self.superadvisor,
            for_client=False,
            for_advisor=True,
            for_superadvisor=True,
            for_manager=False,
            for_administrator=False,
        ) + self.change_user_type_perm_generator(
            user='superadvisor',
            user_modified=self.manager,
            for_client=False,
            for_advisor=False,
            for_superadvisor=False,
            for_manager=False,
            for_administrator=False,
        ) + self.change_user_type_perm_generator(
            user='superadvisor',
            user_modified=self.administrator,
            for_client=False,
            for_advisor=False,
            for_superadvisor=False,
            for_manager=False,
            for_administrator=False,
        )
        # fmt: on
        self.assertPerms(permissions)

    def test_manager_perms(self):
        # fmt: off
        permissions = [
            # View perm
            {'usr': 'manager', 'perm': 'user.view',   'args': (self.client, ),              'result': True},   # NOQA: E501,E241
            {'usr': 'manager', 'perm': 'user.view',   'args': (self.advisor, ),             'result': True},   # NOQA: E501,E241
            {'usr': 'manager', 'perm': 'user.view',   'args': (self.manager, ),             'result': True},   # NOQA: E501,E241
            {'usr': 'manager', 'perm': 'user.view',   'args': (self.administrator, ),       'result': True},   # NOQA: E501,E241
            {'usr': 'manager', 'perm': 'user.view',   'args': (self.other_advisor, ),       'result': True},   # NOQA: E501,E241
            {'usr': 'manager', 'perm': 'user.view',   'args': (self.other_manager, ),       'result': True},   # NOQA: E501,E241
            {'usr': 'manager', 'perm': 'user.view',   'args': (self.other_administrator, ), 'result': True},   # NOQA: E501,E241
            
            # Change perm
            {'usr': 'manager', 'perm': 'user.change', 'args': (self.client, ),              'result': True},   # NOQA: E501,E241
            {'usr': 'manager', 'perm': 'user.change', 'args': (self.advisor, ),             'result': True},   # NOQA: E501,E241
            {'usr': 'manager', 'perm': 'user.change', 'args': (self.manager, ),             'result': True},   # NOQA: E501,E241
            {'usr': 'manager', 'perm': 'user.change', 'args': (self.administrator, ),       'result': False},  # NOQA: E501,E241
            {'usr': 'manager', 'perm': 'user.change', 'args': (self.other_advisor, ),       'result': False},  # NOQA: E501,E241
            {'usr': 'manager', 'perm': 'user.change', 'args': (self.other_manager, ),       'result': False},  # NOQA: E501,E241
            {'usr': 'manager', 'perm': 'user.change', 'args': (self.other_administrator, ), 'result': False},  # NOQA: E501,E241
        ] + self.change_user_type_perm_generator(
            user='manager',
            user_modified=self.client,
            for_client=False,
            for_advisor=False,
            for_superadvisor=False,
            for_manager=False,
            for_administrator=False,
        ) + self.change_user_type_perm_generator(
            user='manager',
            user_modified=self.advisor,
            for_client=False,
            for_advisor=True,
            for_superadvisor=True,
            for_manager=True,
            for_administrator=False,
        ) + self.change_user_type_perm_generator(
            user='manager',
            user_modified=self.superadvisor,
            for_client=False,
            for_advisor=True,
            for_superadvisor=True,
            for_manager=True,
            for_administrator=False,
        ) + self.change_user_type_perm_generator(
            user='manager',
            user_modified=self.manager,
            for_client=False,
            for_advisor=True,
            for_superadvisor=True,
            for_manager=True,
            for_administrator=False,
        ) + self.change_user_type_perm_generator(
            user='manager',
            user_modified=self.administrator,
            for_client=False,
            for_advisor=False,
            for_superadvisor=False,
            for_manager=False,
            for_administrator=False,
        )
        # fmt: on
        self.assertPerms(permissions)

    def test_administrator_perms(self):
        # fmt: off
        permissions = [
            # View perm
            {'usr': 'administrator', 'perm': 'user.view',   'args': (self.client, ),              'result': True},   # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'user.view',   'args': (self.advisor, ),             'result': True},   # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'user.view',   'args': (self.manager, ),             'result': True},   # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'user.view',   'args': (self.administrator, ),       'result': True},   # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'user.view',   'args': (self.other_advisor, ),       'result': True},   # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'user.view',   'args': (self.other_manager, ),       'result': True},   # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'user.view',   'args': (self.other_administrator, ), 'result': True},   # NOQA: E501,E241
            
            # Change perm
            {'usr': 'administrator', 'perm': 'user.change', 'args': (self.client, ),              'result': True},   # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'user.change', 'args': (self.advisor, ),             'result': True},   # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'user.change', 'args': (self.manager, ),             'result': True},   # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'user.change', 'args': (self.administrator, ),       'result': True},   # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'user.change', 'args': (self.other_advisor, ),       'result': True},   # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'user.change', 'args': (self.other_manager, ),       'result': True},   # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'user.change', 'args': (self.other_administrator, ), 'result': True},   # NOQA: E501,E241
        ] + self.change_user_type_perm_generator(
            user='administrator',
            user_modified=self.client,
            for_client=False,
            for_advisor=False,
            for_superadvisor=False,
            for_manager=False,
            for_administrator=False,
        ) + self.change_user_type_perm_generator(
            user='administrator',
            user_modified=self.advisor,
            for_client=False,
            for_advisor=True,
            for_superadvisor=True,
            for_manager=True,
            for_administrator=True,
        ) + self.change_user_type_perm_generator(
            user='administrator',
            user_modified=self.manager,
            for_client=False,
            for_advisor=True,
            for_superadvisor=True,
            for_manager=True,
            for_administrator=True,
        ) + self.change_user_type_perm_generator(
            user='administrator',
            user_modified=self.administrator,
            for_client=False,
            for_advisor=True,
            for_superadvisor=True,
            for_manager=True,
            for_administrator=True,
        )
        # fmt: on
        self.assertPerms(permissions)


class GroupPermTestCase(AssertPermissions, TestCase):
    def setUp(self):
        self.client = ClientProfileFactory()

        self.admin_group = AdminGroupFactory(name="admin group")
        self.other_admin_group = AdminGroupFactory(name="other admin group")

        self.group = GroupFactory(admin_group=self.admin_group, name="Group")
        self.other_group = GroupFactory(
            admin_group=self.other_admin_group, name="Other Group"
        )

        self.advisor = AdvisorProfileFactory(group=self.group)
        self.superadvisor = SuperAdvisorProfileFactory(group=self.group)
        self.manager = ManagerProfileFactory(group=self.admin_group)
        self.administrator = AdministratorProfileFactory(group=self.group)

        self.other_advisor = AdvisorProfileFactory(group=self.other_group)
        self.other_manager = ManagerProfileFactory(group=self.other_admin_group)
        self.other_administrator = AdministratorProfileFactory(group=self.other_group)

        self.group_data = {"name": "Groupe", "admin_group": self.admin_group.pk}
        self.other_group_data = {
            "name": "Autre Groupe",
            "admin_group": self.other_admin_group.pk,
        }

    def test_client_perms(self):
        # fmt: off
        permissions = [
            {'usr': 'client', 'perm': 'group.view',           'args': (self.group, ),        'result': False},  # NOQA: E501,E241
            {'usr': 'client', 'perm': 'group.view',           'args': (self.other_group, ),  'result': False},  # NOQA: E501,E241
            {'usr': 'client', 'perm': 'group.create',         'args': (self.group_data, ),   'result': False},  # NOQA: E501,E241
            {'usr': 'client', 'perm': 'group.change',         'args': (self.group, ),        'result': False},  # NOQA: E501,E241
            {'usr': 'client', 'perm': 'group.change',         'args': (self.other_group, ),  'result': False},  # NOQA: E501,E241
            {'usr': 'client', 'perm': 'group.partial_change', 'args': (self.group, ),        'result': False},  # NOQA: E501,E241
            {'usr': 'client', 'perm': 'group.partial_change', 'args': (self.other_group, ),  'result': False},  # NOQA: E501,E241
        ]
        # fmt: on
        self.assertPerms(permissions)

    def test_advisor_perms(self):
        # fmt: off
        permissions = [
            {'usr': 'advisor', 'perm': 'group.view',           'args': (self.group, ),        'result': True},   # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'group.view',           'args': (self.other_group, ),  'result': True},  # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'group.create',         'args': (self.group_data, ),   'result': False},  # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'group.change',         'args': (self.group, ),        'result': False},  # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'group.change',         'args': (self.other_group, ),  'result': False},  # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'group.partial_change', 'args': (self.group, ),        'result': True},   # NOQA: E501,E241
            {'usr': 'advisor', 'perm': 'group.partial_change', 'args': (self.other_group, ),  'result': False},  # NOQA: E501,E241
        ]
        # fmt: on
        self.assertPerms(permissions)

    def test_superadvisor_perms(self):
        # fmt: off
        permissions = [
            {'usr': 'superadvisor', 'perm': 'group.view',           'args': (self.group, ),        'result': True},   # NOQA: E501,E241
            {'usr': 'superadvisor', 'perm': 'group.view',           'args': (self.other_group, ),  'result': True},  # NOQA: E501,E241
            {'usr': 'superadvisor', 'perm': 'group.create',         'args': (self.group_data, ),   'result': False},  # NOQA: E501,E241
            {'usr': 'superadvisor', 'perm': 'group.change',         'args': (self.group, ),        'result': False},  # NOQA: E501,E241
            {'usr': 'superadvisor', 'perm': 'group.change',         'args': (self.other_group, ),  'result': False},  # NOQA: E501,E241
            {'usr': 'superadvisor', 'perm': 'group.partial_change', 'args': (self.group, ),        'result': True},   # NOQA: E501,E241
            {'usr': 'superadvisor', 'perm': 'group.partial_change', 'args': (self.other_group, ),  'result': False},  # NOQA: E501,E241
        ]
        # fmt: on
        self.assertPerms(permissions)

    def test_manager_perms(self):
        # fmt: off
        permissions = [
            {'usr': 'manager', 'perm': 'group.view',           'args': (self.group, ),            'result': True},   # NOQA: E501,E241
            # {'usr': 'manager', 'perm': 'group.view',           'args': (self.other_group, ),      'result': False},  # NOQA: E501,E241
            # {'usr': 'manager', 'perm': 'group.create',         'args': (self.group_data, ),       'result': True},   # NOQA: E501,E241
            # {'usr': 'manager', 'perm': 'group.create',         'args': (self.other_group_data, ), 'result': False},  # NOQA: E501,E241
            # {'usr': 'manager', 'perm': 'group.change',         'args': (self.group, ),            'result': True},   # NOQA: E501,E241
            # {'usr': 'manager', 'perm': 'group.change',         'args': (self.other_group, ),      'result': False},  # NOQA: E501,E241
            # {'usr': 'manager', 'perm': 'group.partial_change', 'args': (self.group, ),            'result': False},  # NOQA: E501,E241
            # {'usr': 'manager', 'perm': 'group.partial_change', 'args': (self.other_group, ),      'result': False},  # NOQA: E501,E241
        ]
        # fmt: on
        self.assertPerms(permissions)

    def test_administrator_perms(self):
        # fmt: off
        permissions = [
            {'usr': 'administrator', 'perm': 'group.view',           'args': (self.group, ),        'result': True},  # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'group.view',           'args': (self.other_group, ),  'result': True},  # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'group.create',         'args': (self.group_data, ),   'result': True},  # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'group.change',         'args': (self.group, ),        'result': True},  # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'group.change',         'args': (self.other_group, ),  'result': True},  # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'group.partial_change', 'args': (self.group, ),        'result': True},  # NOQA: E501,E241
            {'usr': 'administrator', 'perm': 'group.partial_change', 'args': (self.other_group, ),  'result': True},  # NOQA: E501,E241
        ]
        # fmt: on
        self.assertPerms(permissions)
