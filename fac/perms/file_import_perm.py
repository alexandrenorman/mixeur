# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class FileImportPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, fileimport, *args):
        """
        Permissions for viewing FileImport
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == fileimport.group:
            return True

        return self.admin_permission(user, fileimport, *args)

    change = view
    delete = view
    create = view


register("fileimport", FileImportPermissionLogic)
register("fac/fileimport", FileImportPermissionLogic)
