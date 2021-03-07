# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class ReminderPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, reminder, *args):
        """
        Permissions for viewing Reminder
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == reminder.owning_group:
            return True

        return self.admin_permission(user, reminder, *args)

    def forbidden(self, user, objective, *args):
        return False

    change = forbidden
    delete = forbidden
    create = forbidden


register("reminder", ReminderPermissionLogic)
register("fac/reminder", ReminderPermissionLogic)
