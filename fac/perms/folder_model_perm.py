# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from fac.models import FolderModel

from helpers.mixins import BasicPermissionLogicMixin


class FolderModelPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def create(self, user, foldermodel, *args):
        return False

    def view(self, user, foldermodel, *args):
        """
        Permissions for viewing FolderModel
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor:
            return (
                FolderModel.objects.filter(pk=foldermodel.pk)
                .accessible_by(user)
                .exists()
            )

        return self.admin_permission(user, foldermodel, *args)

    change = create
    delete = create


register("foldermodel", FolderModelPermissionLogic)
register("fac/foldermodel", FolderModelPermissionLogic)
