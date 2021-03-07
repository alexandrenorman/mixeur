# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class PlacePermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, place, *args):
        return True

    def change(self, user, place, *args):
        """
        Permissions for viewing Place
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            if place.inseecode in [x.inseecode for x in user.territories]:
                return True

        if user.is_advisor:
            if "dialogwatt/place.create" in args:
                return True

            if user in place.advisors:
                return True

        return self.admin_permission(user, place, *args)

    delete = change
    create = change


register("dialogwatt/place", PlacePermissionLogic)
