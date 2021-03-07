# -*- coding: utf-8 -*-
from factory import SubFactory, lazy_attribute
from factory.django import DjangoModelFactory

import faker

fake = faker.Factory.create("fr_FR")


class RegionFactory(DjangoModelFactory):
    class Meta:
        model = "territories.Region"

    name = lazy_attribute(lambda o: fake.name())

    inseecode = lazy_attribute(lambda o: fake.postcode())
    geom = lazy_attribute(lambda o: fake.latlng())


class DepartementFactory(DjangoModelFactory):
    class Meta:
        model = "territories.Departement"

    name = lazy_attribute(lambda o: fake.name())
    inseecode = lazy_attribute(lambda o: fake.postcode())
    region = SubFactory(RegionFactory)
    geom = lazy_attribute(lambda o: fake.latlng())


class EpciFactory(DjangoModelFactory):
    class Meta:
        model = "territories.Epci"

    name = lazy_attribute(lambda o: fake.name())
    inseecode = lazy_attribute(lambda o: fake.postcode())
    geom = lazy_attribute(lambda o: fake.latlng())


class CommuneFactory(DjangoModelFactory):
    class Meta:
        model = "territories.Commune"

    name = lazy_attribute(lambda o: fake.name())
    postcode = lazy_attribute(lambda o: fake.postcode())
    inseecode = lazy_attribute(lambda o: fake.postcode())
    departement = SubFactory(DepartementFactory)
    epci = SubFactory(EpciFactory)
    geom = lazy_attribute(lambda o: fake.latlng())
