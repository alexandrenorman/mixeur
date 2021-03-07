# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class SystemPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, system, *args):
        """
        Permissions for viewing System
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return True

        if user.is_advisor:
            return True

        return self.admin_permission(user, system, *args)

    change = view
    delete = view
    create = view


register("system", SystemPermissionLogic)
register("visit_report/system", SystemPermissionLogic)
