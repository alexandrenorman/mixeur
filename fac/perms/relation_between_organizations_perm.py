# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class RelationBetweenOrganizationPermissionLogic(
    BasicPermissionLogicMixin, PermissionLogic
):
    def view(self, user, relationbetweenorganization, *args):
        """
        Permissions for viewing RelationBetweenOrganization
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_manager or user.is_advisor:
            return relationbetweenorganization.owning_group == user.group

        return self.admin_permission(user, relationbetweenorganization, *args)

    def create(self, user, relationbetweenorganization, *args):
        """
        Permissions for creating Organization
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager or user.is_advisor:
            if relationbetweenorganization.owning_group.pk == user.group.pk:
                return True

        return self.admin_permission(user, relationbetweenorganization, *args)

    change = view
    delete = view


register("relationbetweenorganization", RelationBetweenOrganizationPermissionLogic)
register("fac/relationbetweenorganization", RelationBetweenOrganizationPermissionLogic)
