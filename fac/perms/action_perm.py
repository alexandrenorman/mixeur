# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class ActionPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, action, *args):
        """
        Permissions for viewing NoteOrganization
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == action.folder.owning_group:
            return True

        return self.admin_permission(user, action, *args)

    change = view
    delete = view
    create = view


register("action", ActionPermissionLogic)
register("fac/action", ActionPermissionLogic)
