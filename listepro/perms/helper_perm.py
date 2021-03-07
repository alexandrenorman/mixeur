# -*- coding: utf-8 -*-
from helpers.mixins import BasicPermissionLogicMixin

from simple_perms import PermissionLogic, register


class HelperPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, helper, *args):
        """
        Permissions for viewing Helper
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

        return self.admin_permission(user, helper, *args)

    change = view
    delete = view
    create = view


register("listepro/helper", HelperPermissionLogic)
