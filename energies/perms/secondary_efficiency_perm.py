# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class SecondaryEfficiencyPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def change(self, user, secondaryefficiency, *args):
        """
        Permissions for changeing SecondaryEfficiency
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == secondaryefficiency.group:
            return True

        return self.admin_permission(user, secondaryefficiency, *args)

    def view(self, user, secondaryefficiency, *args):
        return True

    delete = change
    create = change


register("energies/secondaryefficiency", SecondaryEfficiencyPermissionLogic)
