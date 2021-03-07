# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class CalendarPermanentUrlPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, calendar_permanent_url, *args):
        """
        Permissions for viewing CalendarPermanentUrl
        """
        if user.is_anonymous:
            return False

        if user.is_client:
            return False

        if user.is_administrator:
            return False

        if user.is_manager:
            return False

        if user.is_advisor:
            if calendar_permanent_url.user_id is None:
                return True
            elif user.is_advisor and user == calendar_permanent_url.user:
                return True

        return self.admin_permission(user, calendar_permanent_url, *args)

    create = view


register("dialogwatt/calendarpermanenturl", CalendarPermanentUrlPermissionLogic)
