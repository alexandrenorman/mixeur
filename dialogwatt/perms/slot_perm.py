# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class SlotPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, slot, *args):
        """
        Permissions for viewing Slot
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == slot.group:
            return True

        return self.admin_permission(user, slot, *args)

    change = view
    delete = view
    create = view


register("dialogwatt/slot", SlotPermissionLogic)
