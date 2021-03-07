# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class FinancialAidPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, financialaid, *args):
        """
        Permissions for viewing FinancialAid
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return True

        if user.is_advisor:
            return True

        return self.admin_permission(user, financialaid, *args)

    change = view
    delete = view
    create = view


register("financialaid", FinancialAidPermissionLogic)
register("visit_report/financialaid", FinancialAidPermissionLogic)
