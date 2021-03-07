# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class BuildingHeatingConsumptionPermissionLogic(
    BasicPermissionLogicMixin, PermissionLogic
):
    def change(self, user, buildingheatingconsumption, *args):
        """
        Permissions for viewing BuildingHeatingConsumption
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        return self.admin_permission(user, buildingheatingconsumption, *args)

    def view(self, user, buildingheatingconsumption, *args):
        return True

    delete = change
    create = change


register(
    "energies/buildingheatingconsumption", BuildingHeatingConsumptionPermissionLogic
)
