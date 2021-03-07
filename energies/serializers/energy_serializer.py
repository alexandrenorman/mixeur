from energies.models import Energy
from helpers.serializers import AutoModelSerializer


class EnergySerializer(AutoModelSerializer):
    model = Energy
    exclude = ["created_at", "updated_at"]
    include_properties = True

    def get_current_price(self, energy):
        if energy.current_price is None:
            return None
        return float(energy.current_price)

    def get_current_price_multi_unit(self, energy):
        if energy.current_price_multi_unit is None:
            return None
        return float(energy.current_price_multi_unit)
