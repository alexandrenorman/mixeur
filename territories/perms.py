# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class CommunePermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, commune, *args):
        return True

    def change(self, user, commune, *args):
        return False

    delete = change
    create = change

    def may_use(self, user, commune, *args):
        """
        User may be allowed to use those communes
        - admin : all
        - manager : those whore are in group.territories
        - advisor : those whore are in admin_group.territories
        """
        if user.is_administrator:
            return True

        if user.is_manager:
            return self.__is_commune_in_allowed_territories_for_manager__(
                user.group, commune
            )

        if user.is_advisor:
            return self.__is_commune_in_allowed_territories_for_manager__(
                user.group.admin_group, commune
            )

        return self.admin_permission(user, commune, *args)

    def can_use(self, user, commune, *args):
        """
        User may be allowed to use those communes
        - admin : all
        - manager : those whore are in group.territories
        - advisor : those whore are in group.territories and admin_group is allowed
        """
        if user.is_administrator or user.is_manager:
            return self.may_use(user, commune, args)

        if user.is_advisor:
            if not self.__is_commune_in_allowed_territories_for_manager__(
                user.group.admin_group, commune
            ):
                return False
            if commune in user.group.territories.all():
                return True

        return self.admin_permission(user, commune, *args)

    def __is_commune_in_allowed_territories_for_manager__(self, manager_group, commune):
        return commune in manager_group.territories.all()


register("commune", CommunePermissionLogic)
register("territories/commune", CommunePermissionLogic)
