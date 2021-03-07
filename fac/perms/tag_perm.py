# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class TagPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, tag, *args):
        """
        Permissions for viewing/editing Tag
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor:
            return tag.owning_group == user.group

        return self.admin_permission(user, tag, *args)

    def create(self, user, tag, *args):
        """
        Permissions for creating Tag
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager or user.is_advisor:
            if tag.owning_group.pk == user.group.pk:
                return True

        return self.admin_permission(user, tag, *args)

    change = view
    delete = view


register("tag", TagPermissionLogic)
register("fac/tag", TagPermissionLogic)
