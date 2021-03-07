# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class AppendixPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, appendix, *args):
        """
        Permissions for viewing Appendix
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == appendix.group:
            return True

        return self.admin_permission(user, appendix, *args)

    change = view
    delete = view
    create = view


register("appendix", AppendixPermissionLogic)
register("visit_report/appendix", AppendixPermissionLogic)
