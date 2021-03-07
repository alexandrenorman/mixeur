# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class ContactsDuplicatePermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, contactsduplicate, *args):
        """
        Permissions for viewing ContactsDuplicate
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == contactsduplicate.group:
            return True

        return self.admin_permission(user, contactsduplicate, *args)

    change = view
    delete = view
    create = view


register("contactsduplicate", ContactsDuplicatePermissionLogic)
register("fac/contactsduplicate", ContactsDuplicatePermissionLogic)
