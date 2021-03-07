# -*- coding: utf-8 -*-
from helpers.serializers import AutoModelSerializer
from fac.models import TypeValorization


class TypeValorizationSerializer(AutoModelSerializer):
    model = TypeValorization

    def get_groups(self, obj):
        """
        get field groups of type ManyToManyField
        """
        groups = obj.groups.all()
        return self._get_pk(groups)
