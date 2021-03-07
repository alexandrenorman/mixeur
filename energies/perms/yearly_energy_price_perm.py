# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class YearlyEnergyPricePermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def change(self, user, yearlyenergyprice, *args):
        """
        Permissions for changeing YearlyEnergyPrice
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == yearlyenergyprice.group:
            return True

        return self.admin_permission(user, yearlyenergyprice, *args)

    def view(self, user, yearlyenergyprice, *args):
        return True

    delete = change
    create = change


register("energies/yearlyenergyprice", YearlyEnergyPricePermissionLogic)
