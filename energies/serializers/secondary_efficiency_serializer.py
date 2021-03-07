import serpy

from energies.models import SecondaryEfficiency
from helpers.serializers import AutoModelSerializer


class SecondaryEfficiencySerializer(AutoModelSerializer):
    model = SecondaryEfficiency
    exclude = ("created_at", "updated_at")
    ratio = serpy.FloatField(required=False)
