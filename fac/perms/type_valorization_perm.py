# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from fac.models import TypeValorization

from helpers.mixins import BasicPermissionLogicMixin


class TypeValorizationPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def create(self, user, typevalorization, *args):
        return False

    def view(self, user, typevalorization, *args):
        """
        Permissions for viewing TypeValorization
        """
        if user.is_anonymous or user.is_client:
            return False

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor:
            return (
                TypeValorization.objects.filter(pk=typevalorization.pk)
                .accessible_by(user)
                .exists()
            )

        return self.admin_permission(user, typevalorization, *args)

    change = create
    delete = create


register("typevalorization", TypeValorizationPermissionLogic)
register("fac/typevalorization", TypeValorizationPermissionLogic)
