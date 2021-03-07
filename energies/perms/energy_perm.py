# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class EnergyPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def change(self, user, energy, *args):
        """
        Permissions for changeing Energy
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == energy.group:
            return True

        return self.admin_permission(user, energy, *args)

    def view(self, user, energy, *args):
        return True

    delete = change
    create = change


register("energies/energy", EnergyPermissionLogic)
