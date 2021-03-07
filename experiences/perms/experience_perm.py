# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class ExperiencePermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, experience, *args):
        """
        Permissions for viewing Experience
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager or user.is_advisor:
            return experience.owning_group.pk == user.group.pk

        return self.admin_permission(user, experience, *args)

    def create(self, user, experience, *args):
        """
        Permissions for creating Experience
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager or user.is_advisor:
            return experience.owning_group.pk == user.group.pk

        return self.admin_permission(user, experience, *args)

    change = view
    delete = view


register("experiences/experience", ExperiencePermissionLogic)
