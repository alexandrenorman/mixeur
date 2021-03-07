# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class ExplanationPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, explanation, *args):
        """
        Permissions for viewing Explanation
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager or user.is_advisor:
            return explanation.owning_group.pk == user.group.pk

        return self.admin_permission(user, explanation, *args)

    create = view
    change = view
    delete = view


register("experiences/explanation", ExplanationPermissionLogic)
