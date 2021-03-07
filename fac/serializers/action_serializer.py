import serpy

from .action_simple_serializer import ActionSimpleSerializer, DocumentsSerializer
from .status_simple_serializer import StatusSimpleSerializer


class ActionLinkedObjectSerializer(serpy.Serializer):
    linked_object = serpy.MethodField()

    def get_linked_object(self, obj):
        linked_object = obj.linked_object
        if obj.folder.content_type.model == "contact":
            name = linked_object.full_name
        else:
            name = linked_object.name
        return {
            "type": obj.folder.content_type.model,
            "pk": obj.folder.object_id,
            "name": name,
            "owning_group": obj.folder.owning_group.pk,
        }

    def get_custom_form_data(self, obj):
        if obj.custom_form_data is None:
            return {}

        return obj.custom_form_data


class ActionSerializer(ActionLinkedObjectSerializer, ActionSimpleSerializer):
    pass


class ActionDocumentSerializer(ActionLinkedObjectSerializer, DocumentsSerializer):
    date = serpy.MethodField()

    def get_date(self, action):
        return action.date


class ActionFolderSerializer(ActionSerializer):
    folder_status = serpy.MethodField()
    folder_name = serpy.MethodField()

    def get_folder_status(self, obj):
        status = obj.folder.get_status()
        if status:
            return StatusSimpleSerializer(status).data
        return None

    def get_folder_name(self, obj):
        return obj.folder.model.name
