import serpy

from energies.models import ProductionSystem
from helpers.serializers import AutoModelSerializer


class ProductionSystemSerializer(AutoModelSerializer):
    model = ProductionSystem
    exclude = ["energy", "created_at", "updated_at"]
    energy_id = serpy.Field()
    name = serpy.Field()

    def get_energy_identifier(self, production_system):
        return production_system.energy.identifier
