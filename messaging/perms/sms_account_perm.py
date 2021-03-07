# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class SmsAccountPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, smsaccount, *args):
        """
        Permissions for viewing SmsAccount
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return False

        if user.is_manager:
            return False

        if user.is_superadvisor and user.group == smsaccount.group:
            return True

        return self.admin_permission(user, smsaccount, *args)

    change = view
    delete = view
    create = view


register("messaging/smsaccount", SmsAccountPermissionLogic)
