# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class ProductionSystemPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def change(self, user, productionsystem, *args):
        """
        Permissions for changeing ProductionSystem
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == productionsystem.group:
            return True

        return self.admin_permission(user, productionsystem, *args)

    def view(self, user, productionsystem, *args):
        return True

    delete = change
    create = change


register("energies/productionsystem", ProductionSystemPermissionLogic)
