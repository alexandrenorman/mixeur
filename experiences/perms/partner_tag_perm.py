# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class PartnerTagPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, partnertag, *args):
        """
        Permissions for viewing PartnerTag
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_manager or user.is_advisor:
            return partnertag.owning_group.pk == user.group.pk

        return self.admin_permission(user, partnertag, *args)

    change = view
    delete = view
    create = view


register("experiences/partnertag", PartnerTagPermissionLogic)
