# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class DidActionPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, action, *args):
        """
        Permissions for viewing DidAction
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        # TODO check groups in request maybe ? dunno
        if user.is_advisor:
            return True

        return self.admin_permission(user, action, *args)


register("did_action", DidActionPermissionLogic)
register("fac/did_action", DidActionPermissionLogic)
