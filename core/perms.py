# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic
from helpers.mixins import BasicPermissionLogicMixin


class MixeurPermissionLogicMixin(BasicPermissionLogicMixin, PermissionLogic):
    """
    Permissions for accessing Obj

    - anonymous : False
    - client: False
    - administrator: True
    - manager: True
    - advisor : True if obj.group == user.group
    """

    def view(self, user, obj, *args):
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        try:
            if user.is_advisor and user.group == obj.group:
                return True
        except AttributeError:
            return False

        return self.admin_permission(user, obj, *args)

    change = view
    delete = view
    create = view
