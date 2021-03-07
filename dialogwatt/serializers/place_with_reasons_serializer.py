import serpy

from .place_serializer import PlaceSerializer
from .reason_serializer import ReasonSimpleSerializer


class PlaceWithReasonsSerializer(serpy.Serializer):
    place = PlaceSerializer(required=True)
    reasons = ReasonSimpleSerializer(many=True)
