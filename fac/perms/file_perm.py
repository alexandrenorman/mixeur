# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class FilePermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, file, *args):
        """
        Permissions for viewing FileOrganization
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == file.owning_group:
            return True

        return self.admin_permission(user, file, *args)

    change = view
    delete = view
    create = view


register("file", FilePermissionLogic)
register("fac/file", FilePermissionLogic)
