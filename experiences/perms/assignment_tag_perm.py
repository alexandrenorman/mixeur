# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class AssignmentTagPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, assignmenttag, *args):
        """
        Permissions for viewing AssignmentTag
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_manager or user.is_advisor:
            return assignmenttag.owning_group.pk == user.group.pk

        return self.admin_permission(user, assignmenttag, *args)

    change = view
    delete = view
    create = view


register("experiences/assignmenttag", AssignmentTagPermissionLogic)
