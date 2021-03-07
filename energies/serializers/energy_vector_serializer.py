import serpy

from energies.models import EnergyVector
from helpers.serializers import AutoModelSerializer


class EnergyVectorSerializer(AutoModelSerializer):
    model = EnergyVector
    exclude = ("energy", "updated_at", "created_at")
    energy_id = serpy.Field()

    def get_energy_identifier(self, energy_vector):
        return energy_vector.energy.identifier
