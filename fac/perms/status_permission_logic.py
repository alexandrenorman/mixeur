from simple_perms import PermissionLogic, register

from fac.models import Project
from helpers.mixins import BasicPermissionLogicMixin


class StatusPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, status, *args):
        """
        Permissions for viewing Status
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor:
            return Project.objects.filter(folder_models__statuses=status).accessible_by(
                user
            )

        return self.admin_permission(user, status, *args)

    def forbidden(self, user, objective, *args):
        return False

    change = forbidden
    delete = forbidden
    create = forbidden


register("fac/status", StatusPermissionLogic)
