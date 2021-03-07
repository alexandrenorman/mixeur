# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from fac.models import Project
from helpers.mixins import BasicPermissionLogicMixin


class ProjectPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, project, *args):
        """
        Permissions for viewing Project
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor:
            return Project.objects.filter(pk=project.pk).accessible_by(user).exists()

        return self.admin_permission(user, project, *args)

    @staticmethod
    def forbidden(user, project, *args):
        return False

    change = forbidden
    delete = forbidden
    create = forbidden


register("fac/project", ProjectPermissionLogic)
