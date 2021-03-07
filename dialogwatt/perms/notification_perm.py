# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class NotificationPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, notification, *args):
        """
        Permissions for viewing Notification
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == notification.group:
            return True

        return self.admin_permission(user, notification, *args)

    change = view
    delete = view
    create = view


register("dialogwatt/notification", NotificationPermissionLogic)
