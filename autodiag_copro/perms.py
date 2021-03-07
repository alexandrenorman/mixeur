# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class DiagnosticPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, diagnostic, *args):
        if user.is_client:
            if user == diagnostic.user:
                return True
            return False

        if user.is_advisor:
            return True

        return self.admin_and_manager_permission(user, diagnostic, *args)

    def change(self, user, diagnostic, *args):
        if user.is_client:
            if user == diagnostic.user:
                return True
            return False

        if user.is_advisor:
            return True

        return self.admin_and_manager_permission(user, diagnostic, *args)

    def delete(self, user, diagnostic, *args):
        if user.is_client:
            if user == diagnostic.user:
                return True
            return False

        if user.is_advisor:
            return True

        return self.admin_and_manager_permission(user, diagnostic, *args)


register("autodiagCopro", DiagnosticPermissionLogic)
