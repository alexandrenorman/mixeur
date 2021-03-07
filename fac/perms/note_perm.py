# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class NotePermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, note, *args):
        """
        Permissions for viewing NoteOrganization
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == note.owning_group:
            return True

        return self.admin_permission(user, note, *args)

    change = view
    delete = view
    create = view


register("note", NotePermissionLogic)
register("fac/note", NotePermissionLogic)
