# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class CarbonTaxPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def change(self, user, carbontax, *args):
        """
        Permissions for changeing CarbonTax
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == carbontax.group:
            return True

        return self.admin_permission(user, carbontax, *args)

    def view(self, user, carbontax, *args):
        return True

    delete = change
    create = change


register("energies/carbontax", CarbonTaxPermissionLogic)
