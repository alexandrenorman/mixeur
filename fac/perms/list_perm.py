# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class ListPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, fac_list, *args):
        """
        Permissions for viewing List
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == fac_list.owning_group:
            return True

        return self.admin_permission(user, fac_list, *args)

    change = view
    delete = view
    create = view


register("list", ListPermissionLogic)
register("fac/list", ListPermissionLogic)
