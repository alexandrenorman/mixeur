# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class SmtpAccountPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, smtpaccount, *args):
        """
        Permissions for viewing SmtpAccount
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return False

        if user.is_manager:
            return False

        if user.is_superadvisor and user.group == smtpaccount.group:
            return True

        return self.admin_permission(user, smtpaccount, *args)

    change = view
    delete = view
    create = view


register("messaging/smtpaccount", SmtpAccountPermissionLogic)
