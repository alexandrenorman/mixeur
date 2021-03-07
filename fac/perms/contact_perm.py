# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class ContactPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, contact, *args):
        """
        Permissions for viewing Contact
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager or user.is_advisor:
            return contact.owning_group == user.group

        return self.admin_permission(user, contact, *args)

    def create(self, user, contact, *args):
        """
        Permissions for creating Contact
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager or user.is_advisor:
            if contact.owning_group.pk == user.group.pk:
                return True

        return self.admin_permission(user, contact, *args)

    change = view
    delete = view


register("contact", ContactPermissionLogic)
register("fac/contact", ContactPermissionLogic)
