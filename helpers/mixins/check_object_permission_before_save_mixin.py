import uuid


class CheckObjectPermissionBeforeSaveMixin:
    def create(self, request, *args, **kwargs):
        self.check_instance_from_data_permission(request)
        return super(CheckObjectPermissionBeforeSaveMixin, self).create(
            request, *args, **kwargs
        )

    def update(self, request, *args, **kwargs):
        self.check_instance_from_data_permission(request)
        return super(CheckObjectPermissionBeforeSaveMixin, self).update(
            request, *args, **kwargs
        )

    def destroy(self, request, *args, **kwargs):
        self.check_instance_from_data_permission(request)
        return super(CheckObjectPermissionBeforeSaveMixin, self).destroy(
            request, *args, **kwargs
        )

    def check_instance_from_data_permission(self, request):
        instance = self.get_instance_from_data(request.data)
        if instance:
            self.check_object_permissions(request, instance)

    def get_instance_from_data(self, data):
        ModelClass = self.serializer_class.Meta.model
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            instance = ModelClass(**serializer.validated_data)
            instance.id = (
                data.get("id") or uuid.uuid4().hex
            )  # Django's has_perm need a primary key to be set...
            return instance
        return None
