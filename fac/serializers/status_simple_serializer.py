from fac.models import Status
from helpers.serializers import AutoModelSerializer


class StatusSimpleSerializer(AutoModelSerializer):
    model = Status
    exclude = ["folder_model", "order"]
