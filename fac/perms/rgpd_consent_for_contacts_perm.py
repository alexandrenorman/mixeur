# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class RgpdConsentForContactsPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, rgpdconsentforcontacts, *args):
        """
        Permissions for viewing RgpdConsentForContacts
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == rgpdconsentforcontacts.group:
            return True

        return self.admin_permission(user, rgpdconsentforcontacts, *args)

    change = view
    delete = view
    create = view


register("rgpdconsentforcontacts", RgpdConsentForContactsPermissionLogic)
register("fac/rgpdconsentforcontacts", RgpdConsentForContactsPermissionLogic)
