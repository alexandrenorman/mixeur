# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class AbstractTagPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, abstracttag, *args):
        """
        Permissions for viewing AbstractTag
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == abstracttag.group:
            return True

        return self.admin_permission(user, abstracttag, *args)

    change = view
    delete = view
    create = view


register("experiences/abstracttag", AbstractTagPermissionLogic)
