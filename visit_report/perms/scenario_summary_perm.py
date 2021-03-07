# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class ScenarioSummaryPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, scenariosummary, *args):
        """
        Permissions for viewing ScenarioSummary
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return True

        if user.is_advisor:
            return True

        return self.admin_permission(user, scenariosummary, *args)

    change = view
    delete = view
    create = view


register("scenariosummary", ScenarioSummaryPermissionLogic)
register("visit_report/scenariosummary", ScenarioSummaryPermissionLogic)
