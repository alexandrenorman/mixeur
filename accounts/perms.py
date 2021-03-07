# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class UserPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, user_to_view, *args):
        if user_to_view == user:
            return True

        if user.is_client or user.is_professional:
            return False
        if user.is_administrator or user.is_advisor or user.is_manager:
            return True

        return self.admin_permission(user, user_to_view, *args)

    def change(self, user, user_to_modify, *args):
        if user_to_modify == user:
            return True

        if user.is_client or user.is_professional:
            return False

        if user.is_administrator:
            return True

        # Allow same group modifications
        if user_to_modify.group is not None and user_to_modify.group.is_member(user):
            if user.is_advisor and user_to_modify.is_advisor:
                return True
            if user.is_manager and (
                user_to_modify.is_advisor or user_to_modify.is_manager
            ):
                return True

        if (user.is_advisor or user.is_manager) and user_to_modify.is_client:
            return True

        if (
            user.is_manager
            and user_to_modify.is_advisor
            and user_to_modify.group.admin_group == user.group
            and user.group.is_admin
        ):
            return True

        if (
            user.is_manager
            and user_to_modify.is_manager
            and user_to_modify.group == user.group
        ):
            return True

        return self.admin_permission(user, user_to_modify, *args)

    def change_user_type(self, user, *args):
        """
        Perm for user to change user_type for user_modified

        Parameters
        ----------
        user : User
        args : Dict(user_modified, to_user_type)
        """
        user_modified = args[0]["user_modified"]
        to_user_type = args[0]["to_user_type"]

        if user.is_client or user.is_professional:
            return False

        if user_modified.is_client or user_modified.is_professional:
            return False

        if to_user_type == "client" or to_user_type == "professional":
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            if (
                user_modified.is_advisor
                or user_modified.is_superadvisor
                or user_modified.is_manager
                and user_modified.group.is_member(user)
            ):
                if to_user_type in ["advisor", "superadvisor", "manager"]:
                    return True

        if (
            user.is_superadvisor
            and to_user_type in ["advisor", "superadvisor"]
            and user_modified.is_advisor
        ):
            return True

        return self.admin_permission(user, user_modified, *args)


register("user", UserPermissionLogic)
register("accounts/user", UserPermissionLogic)


class RgpdConsentPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, rgpdconsent, *args):
        if rgpdconsent.user == user:
            return True

        return self.admin_permission(user, rgpdconsent, *args)

    change = view


register("rgpdconsent", RgpdConsentPermissionLogic)
register("accounts/rgpdconsent", RgpdConsentPermissionLogic)


class GroupPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, group, *args):
        if user.is_anonymous:
            return False

        if user.is_administrator:
            return True

        if user.is_advisor or user.is_manager:
            return True

        return self.admin_permission(user, group, *args)

    def create(self, user, group, group_data, *args):
        if user.is_anonymous:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            if not group_data:
                return False

            if user.group is not None:
                if group is not None:
                    if group.admin_group.pk == user.group.pk:
                        return True

        return self.admin_permission(user, None, *args)

    def change(self, user, group, *args):
        if user.is_anonymous:
            return False

        if user.is_administrator:
            return True

        if (
            user.is_manager
            and user.group is not None
            and group.admin_group == user.group
        ):
            return True

        return self.admin_permission(user, group, *args)

    def partial_change(self, user, group, *args):
        """
        change only some fiels on group
        """
        if user.is_advisor and user.group is not None and group == user.group:
            return True

        return self.admin_permission(user, group, *args)


register("group", GroupPermissionLogic)
register("accounts/group", GroupPermissionLogic)


class GroupPlacePermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, group, *args):
        if user.is_anonymous:
            return False

        if user.is_expert:
            return True

        return self.admin_permission(user, group, *args)


register("group_place", GroupPlacePermissionLogic)
register("accounts/group_place", GroupPlacePermissionLogic)
