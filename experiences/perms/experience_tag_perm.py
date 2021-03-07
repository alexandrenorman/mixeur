# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class ExperienceTagPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, experiencetag, *args):
        """
        Permissions for viewing ExperienceTag
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_manager or user.is_advisor:
            return experiencetag.owning_group.pk == user.group.pk

        return self.admin_permission(user, experiencetag, *args)

    change = view
    delete = view
    create = view


register("experiences/experiencetag", ExperienceTagPermissionLogic)
