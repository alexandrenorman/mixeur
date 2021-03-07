# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class HousingPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, housing, *args):
        """
        Permissions for viewing Housing
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return True

        if user.is_advisor:
            return True

        return self.admin_permission(user, housing, *args)

    change = view
    delete = view
    create = view


register("housing", HousingPermissionLogic)
register("visit_report/housing", HousingPermissionLogic)
