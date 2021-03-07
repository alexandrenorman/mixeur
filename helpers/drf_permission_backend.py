from rest_framework.permissions import DjangoObjectPermissions


class APrioriDjangoObjectPermissions(DjangoObjectPermissions):
    def __is_authenticated__(self, user):
        return user.is_authenticated

    def has_permission(self, request, view, *args, **kwargs):
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        if getattr(view, "_ignore_model_permissions", False):
            return True

        if not request.user or not self.__is_authenticated__(request.user):
            return False

        return super(APrioriDjangoObjectPermissions, self).has_permission(
            request, view, *args, **kwargs
        )

    # def has_object_permission(self, request, view, obj):
    #    Need to implement same mecanisme in has_object_permission ?
