# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class OrganizationPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, organization, *args):
        """
        Permissions for viewing Organization
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager or user.is_advisor:
            return organization.owning_group == user.group

        return self.admin_permission(user, organization, *args)

    def create(self, user, organization, *args):
        """
        Permissions for creating Organization
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager or user.is_advisor:
            if organization.owning_group.pk == user.group.pk:
                return True

        return self.admin_permission(user, organization, *args)

    change = view
    delete = view


register("organization", OrganizationPermissionLogic)
register("fac/organization", OrganizationPermissionLogic)
