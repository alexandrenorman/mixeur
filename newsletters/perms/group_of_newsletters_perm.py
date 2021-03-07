# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin

from newsletters.models import GroupOfNewsletters


class GroupOfNewslettersPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, groupofnewsletters, *args):
        """
        Permissions for viewing GroupOfNewsletters
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return False

        if user.is_manager:
            return False

        if user.is_advisor:
            return (
                GroupOfNewsletters.objects.filter(pk=groupofnewsletters.pk)
                .accessible_by(user)
                .exists()
            )

        return self.admin_permission(user, groupofnewsletters, *args)

    def create(self, user, groupofnewsletters, *args):
        """
        Permissions for creating Groupofnewsletters
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager or user.is_advisor:
            if groupofnewsletters.group.pk == user.group.pk:
                return True

    change = view
    delete = view


register("newsletters/groupofnewsletters", GroupOfNewslettersPermissionLogic)


class GroupOfNewslettersPublicPermissionLogic(
    BasicPermissionLogicMixin, PermissionLogic
):
    def view(self, user, groupofnewsletters, *args):
        return True

    def create(self, user, groupofnewsletters, *args):
        return False

    change = create
    delete = create


register(
    "newsletters/groupofnewsletterspublic", GroupOfNewslettersPublicPermissionLogic
)
