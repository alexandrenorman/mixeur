# -*- coding: utf-8 -*-
from helpers.mixins import BasicPermissionLogicMixin

from simple_perms import PermissionLogic, register


class ProfessionalPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, professional, *args):
        """
        Permissions for viewing Professional
        """
        if user.is_anonymous or user.is_client:
            return True

        if user.is_professional:
            return True

        if user.is_administrator:
            return True

        if user.is_manager:
            return True

        if user.is_advisor:
            return True

        return self.admin_permission(user, professional, *args)

    def create(self, user, professional, *args):
        """
        Permissions for creating Professional
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_professional:
            return True

        if user.is_administrator:
            return True

        if user.is_advisor:
            return True

        return self.admin_permission(user, professional, *args)

    def change(self, user, professional, *args):
        """
        Permissions for creating Professional
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_professional:
            return True

        if user.is_administrator:
            return True

        if user.is_advisor:
            return True

        return self.admin_permission(user, professional, *args)

    delete = view


register("listepro/professional", ProfessionalPermissionLogic)
