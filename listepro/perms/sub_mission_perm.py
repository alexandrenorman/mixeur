# -*- coding: utf-8 -*-
from helpers.mixins import BasicPermissionLogicMixin

from simple_perms import PermissionLogic, register


class SubMissionPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, submission, *args):
        """
        Permissions for viewing SubMission
        """
        if user.is_anonymous or user.is_client:
            return True

        if user.is_professional:
            return True

        if user.is_administrator:
            return True

        if user.is_manager:
            return True

        if user.is_advisor:
            return True

        return self.admin_permission(user, submission, *args)

    change = view
    delete = view
    create = view


register("listepro/submission", SubMissionPermissionLogic)
