import serpy

from .contactable_serializer import ContactableSerializer
from .action_model_serializer import ActionModelSerializer


class DidActionSerializer(ActionModelSerializer):
    contactables_with_this_action_model = serpy.MethodField()

    def get_contactables_with_this_action_model(self, action_model):
        return [
            ContactableSerializer(folder.linked_object).data
            for folder in action_model.folders
        ]
