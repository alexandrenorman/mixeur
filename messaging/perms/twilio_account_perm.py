# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class TwilioAccountPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, twilioaccount, *args):
        """
        Permissions for viewing TwilioAccount
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return False

        if user.is_manager:
            return False

        if user.is_superadvisor and user.group == twilioaccount.group:
            return True

        return self.admin_permission(user, twilioaccount, *args)

    change = view
    delete = view
    create = view


register("messaging/twilioaccount", TwilioAccountPermissionLogic)
