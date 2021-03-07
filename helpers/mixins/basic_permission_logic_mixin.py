# -*- coding: utf-8 -*-


class BasicPermissionLogicMixin:
    """
    Basic permissions logic mixin for admin, managers and accountants
    """

    def admin_permission(self, user, *args):
        return user.is_administrator

    def admin_and_manager_permission(self, user, *args):
        return user.is_administrator or user.is_manager

    def admin_and_manager_and_advisor_permission(self, user, *args):
        return user.is_administrator or user.is_manager or user.is_advisor
