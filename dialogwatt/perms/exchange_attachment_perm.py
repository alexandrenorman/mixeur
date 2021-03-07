# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class ExchangeAttachmentPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, exchangeattachment, *args):
        """
        Permissions for viewing ExchangeAttachment
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == exchangeattachment.group:
            return True

        return self.admin_permission(user, exchangeattachment, *args)

    change = view
    delete = view
    create = view


register("dialogwatt/exchangeattachment", ExchangeAttachmentPermissionLogic)
