# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin

from newsletters.models import Image


class ImagePermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, image, *args):
        """
        Permissions for viewing Image
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return False

        if user.is_manager:
            return False

        if user.is_advisor:
            return Image.objects.filter(pk=image.pk).accessible_by(user).exists()

        return self.admin_permission(user, image, *args)

    def create(self, user, image, *args):
        """
        Permissions for creating image
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager or user.is_advisor:
            if image.group.pk == user.group.pk:
                return True

    change = view
    delete = view


register("newsletters/image", ImagePermissionLogic)
