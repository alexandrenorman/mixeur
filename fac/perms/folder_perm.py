# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class FolderPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, folder, *args):
        """
        Permissions for viewing/editing Folder
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor:
            return folder.owning_group == user.group

        return self.admin_permission(user, folder, *args)

    def create(self, user, folder, *args):
        """
        Permissions for creating Folder
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager or user.is_advisor:
            if folder.owning_group.pk == user.group.pk:
                return True

        return self.admin_permission(user, folder, *args)

    change = view
    delete = view


register("folder", FolderPermissionLogic)
register("fac/folder", FolderPermissionLogic)
