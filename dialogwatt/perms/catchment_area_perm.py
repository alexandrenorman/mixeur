# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class CatchmentAreaPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, catchment_area, *args):
        """
        Permissions for viewing CatchmentArea
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor:
            if catchment_area.group == user.group:
                return True

        return self.admin_permission(user, catchment_area, *args)

    change = view
    delete = view
    create = view


register("dialogwatt/catchment_area", CatchmentAreaPermissionLogic)
