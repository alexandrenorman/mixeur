from energies.models import BuildingHeatingConsumption
from helpers.serializers import AutoModelSerializer


class BuildingHeatingConsumptionSerializer(AutoModelSerializer):
    model = BuildingHeatingConsumption
    exclude = ["created_at", "updated_at"]
    include_properties = True
