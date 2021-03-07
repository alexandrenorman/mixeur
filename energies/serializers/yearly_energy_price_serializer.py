import serpy
from .energy_serializer import EnergySerializer


class YearlyEnergyPriceSerializer(serpy.Serializer):
    id = serpy.IntField()
    year = serpy.IntField()
    price = serpy.FloatField()
    energy = EnergySerializer()
