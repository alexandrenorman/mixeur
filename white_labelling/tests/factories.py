# -*- coding: utf-8 -*-
from factory.django import DjangoModelFactory
from factory.helpers import lazy_attribute_sequence


class WhiteLabellingFactory(DjangoModelFactory):
    class Meta:
        model = "white_labelling.WhiteLabelling"

    @lazy_attribute_sequence
    def domain(self, n):
        return f"test-{n}.org"
