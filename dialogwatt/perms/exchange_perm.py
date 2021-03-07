# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class ExchangePermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, exchange, *args):
        """
        Permissions for viewing Exchange
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor:
            if exchange.group and exchange.group == user.group:
                return True

        return self.admin_permission(user, exchange, *args)


register("dialogwatt/exchange", ExchangePermissionLogic)
