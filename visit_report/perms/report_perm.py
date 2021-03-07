# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class ReportPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, visitreport, *args):
        """
        Permissions for viewing Report
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return True

        # if user.is_advisor and user.group == visitreport.group:
        if user.is_advisor:
            return True

        return self.admin_permission(user, visitreport, *args)

    def create(self, user, visitreport, *args):
        if user.is_advisor:
            return True

        return self.view(user, visitreport, *args)

    change = view
    delete = view


register("report", ReportPermissionLogic)
register("visit_report/report", ReportPermissionLogic)
