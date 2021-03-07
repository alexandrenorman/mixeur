# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class JobTagPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, jobtag, *args):
        """
        Permissions for viewing JobTag
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_manager or user.is_advisor:
            return jobtag.owning_group.pk == user.group.pk

        return self.admin_permission(user, jobtag, *args)

    change = view
    delete = view
    create = view


register("experiences/jobtag", JobTagPermissionLogic)
