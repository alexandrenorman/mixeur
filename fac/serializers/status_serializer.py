import serpy

from .contactable_serializer import ContactableSerializer
from .status_simple_serializer import StatusSimpleSerializer


class StatusSerializer(StatusSimpleSerializer):
    contactables_with_this_status = serpy.MethodField()

    def get_contactables_with_this_status(self, status):
        return [
            ContactableSerializer(folder.linked_object).data
            for folder in status.status_folders
        ]
