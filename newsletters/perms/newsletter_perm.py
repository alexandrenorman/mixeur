# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin

from newsletters.models import Newsletter


class NewsletterPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, newsletter, *args):
        """
        Permissions for viewing Newsletter
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return False

        if user.is_manager:
            return False

        if user.is_advisor:
            return (
                Newsletter.objects.filter(pk=newsletter.pk).accessible_by(user).exists()
            )

        return self.admin_permission(user, newsletter, *args)

    def create(self, user, newsletter, *args):
        """
        Permissions for creating newsletter
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager or user.is_advisor:
            if user.group.pk == newsletter.group_of_newsletters.group.pk:
                return True

    change = view
    delete = view


register("newsletters/newsletter", NewsletterPermissionLogic)
