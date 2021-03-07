# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class NotificationRequestedPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, notificationrequested, *args):
        """
        Permissions for viewing NotificationRequested
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == notificationrequested.group:
            return True

        return self.admin_permission(user, notificationrequested, *args)

    change = view
    delete = view
    create = view


register("dialogwatt/notificationrequested", NotificationRequestedPermissionLogic)
