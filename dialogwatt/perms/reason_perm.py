# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class ReasonPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, reason, *args):
        """
        Permissions for viewing Reason
        """
        if user.is_anonymous or user.is_client:
            return True

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == reason.group:
            return True

        return self.admin_permission(user, reason, *args)

    change = view
    delete = view
    create = view


register("dialogwatt/reason", ReasonPermissionLogic)
