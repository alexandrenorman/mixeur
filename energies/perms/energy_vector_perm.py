# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class EnergyVectorPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def change(self, user, energyvector, *args):
        """
        Permissions for changeing EnergyVector
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == energyvector.group:
            return True

        return self.admin_permission(user, energyvector, *args)

    def view(self, user, energyvector, *args):
        return True

    delete = change
    create = change


register("energies/energyvector", EnergyVectorPermissionLogic)
