# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class IncompleteModelPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, incomplete_model, *args):
        """
        Permissions for viewing Incomplete_Model
        """
        if user.is_advisor and user.group == incomplete_model.owning_group:
            return True

        return self.admin_permission(user, incomplete_model, *args)

    def create(self, user, incomplete_model, *args):
        return False

    change = create
    delete = create


register("fac/incomplete_model", IncompleteModelPermissionLogic)
