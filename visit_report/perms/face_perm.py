# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class FacePermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, face, *args):
        """
        Permissions for viewing Face
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return True

        if user.is_advisor:
            return True

        return self.admin_permission(user, face, *args)

    change = view
    delete = view
    create = view


register("face", FacePermissionLogic)
register("visit_report/face", FacePermissionLogic)
