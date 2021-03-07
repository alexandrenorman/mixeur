# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from helpers.mixins import BasicPermissionLogicMixin


class WorkRecommendationPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, workrecommendation, *args):
        """
        Permissions for viewing WorkRecommendation
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return True

        if user.is_advisor:
            return True

        return self.admin_permission(user, workrecommendation, *args)

    change = view
    delete = view
    create = view


register("workrecommendation", WorkRecommendationPermissionLogic)
register("visit_report/workrecommendation", WorkRecommendationPermissionLogic)
