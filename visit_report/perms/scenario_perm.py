# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class ScenarioPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, scenario, *args):
        """
        Permissions for viewing Scenario
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return True

        if user.is_advisor:
            return True

        return self.admin_permission(user, scenario, *args)

    change = view
    delete = view
    create = view


register("scenario", ScenarioPermissionLogic)
register("visit_report/scenario", ScenarioPermissionLogic)
