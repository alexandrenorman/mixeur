# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class StepPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, step, *args):
        """
        Permissions for viewing Step
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return True

        if user.is_advisor:
            return True

        return self.admin_permission(user, step, *args)

    change = view
    delete = view
    create = view


register("step", StepPermissionLogic)
register("visit_report/step", StepPermissionLogic)
