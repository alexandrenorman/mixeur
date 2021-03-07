# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class FinancingPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, financing, *args):
        """
        Permissions for viewing Financing
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return True

        if user.is_advisor:
            return True

        return self.admin_permission(user, financing, *args)

    change = view
    delete = view
    create = view


register("financing", FinancingPermissionLogic)
register("visit_report/financing", FinancingPermissionLogic)
