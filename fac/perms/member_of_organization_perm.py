# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class MemberOfOrganizationPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, memberoforganization, *args):
        """
        Permissions for viewing MemberOfOrganization
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == memberoforganization.owning_group:
            return True

        return self.admin_permission(user, memberoforganization, *args)

    change = view
    delete = view
    create = view


register("memberoforganization", MemberOfOrganizationPermissionLogic)
register("fac/memberoforganization", MemberOfOrganizationPermissionLogic)
