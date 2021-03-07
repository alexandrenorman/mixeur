# -*- coding: utf-8 -*-
from helpers.mixins import BasicPermissionLogicMixin

from simple_perms import PermissionLogic, register


class ActivityPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, activity, *args):
        """
        Permissions for viewing Activity
        """

        if user.is_anonymous or user.is_client:
            return True

        if user.is_professional:
            return True

        if user.is_administrator:
            return True

        if user.is_manager:
            return True

        if user.is_advisor:
            return True

        return self.admin_permission(user, activity, *args)

    change = view
    delete = view
    create = view


register("listepro/activity", ActivityPermissionLogic)
