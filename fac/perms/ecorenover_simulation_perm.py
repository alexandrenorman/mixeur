# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class EcorenoverSimulationPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, ecorenover_simulation, *args):
        """
        Permissions for viewing EcorenoverSimulation
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == ecorenover_simulation.owning_group:
            return True

        return self.admin_permission(user, ecorenover_simulation, *args)

    change = view
    delete = view
    create = view


register("ecorenover_simulation", EcorenoverSimulationPermissionLogic)
register("fac/ecorenover_simulation", EcorenoverSimulationPermissionLogic)
