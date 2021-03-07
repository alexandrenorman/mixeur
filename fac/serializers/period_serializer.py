from helpers.serializers import AutoModelSerializer
from fac.models import Period


class PeriodSerializer(AutoModelSerializer):
    model = Period
