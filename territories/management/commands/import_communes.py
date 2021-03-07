from django.core.management.base import BaseCommand
from config import settings
from territories.models import Commune, Departement, Region, Epci
import shapefile
import json


class Command(BaseCommand):

    help = "Import shapefile des territoires"

    def handle(self, *args, **options):

        path = settings.BASE_DIR + "/territories/shapefile/REGION.shp"
        print(path)

        reader = shapefile.Reader(path)
        for row in reader.iterRecords():
            name = row[1]
            inseecode = row[2]
            region, created = Region.objects.update_or_create(
                inseecode=inseecode, defaults={"name": name}
            )

        path = settings.BASE_DIR + "/territories/shapefile/DEPARTEMENT.shp"
        print(path)

        reader = shapefile.Reader(path)
        for row in reader.iterRecords():
            name = row[1]
            inseecode = row[2]
            region = Region.objects.get(inseecode=row[3])
            departement, created = Departement.objects.update_or_create(
                inseecode=inseecode, defaults={"name": name, "region": region}
            )

        path = settings.BASE_DIR + "/territories/shapefile/EPCI.shp"
        print(path)

        reader = shapefile.Reader(path, encoding="latin1")
        for row in reader.iterRecords():
            name = row[2].decode("latin1") if row[2].__class__ == bytes else row[2]
            inseecode = row[1]
            region, created = Epci.objects.update_or_create(
                inseecode=inseecode, defaults={"name": name}
            )

        path = settings.BASE_DIR + "/territories/shapefile/COMMUNE.shp"
        print(path)

        reader = shapefile.Reader(path, encoding="latin1")
        for row in reader.iterRecords():

            name = row[3].decode("latin1") if row[3].__class__ == bytes else row[3]
            inseecode = row[2]

            try:
                departement = Departement.objects.get(inseecode=row[6])

                if Epci.objects.filter(inseecode=row[9]).exists():
                    epci = Epci.objects.get(inseecode=row[9])
                else:
                    epci = None
                    print(f"{name} has no EPCI")

                commune, created = Commune.objects.update_or_create(
                    inseecode=inseecode,
                    defaults={"name": name, "departement": departement, "epci": epci},
                )
            except Exception:
                print(
                    "ERROR {} : {} - {} - EPCI {}".format(
                        inseecode, name, row[6], row[9]
                    )
                )

        path = settings.BASE_DIR + "/territories/shapefile/EPCI_POINT.geojson"
        with open(path) as json_data:
            data_dict = json.load(json_data)

        for feature in data_dict["features"]:
            epci = Epci.objects.get(inseecode=feature["properties"]["CODE_EPCI"])
            epci.geom = feature["geometry"]


#
# ['EU_circo',
#  'code_région',
#  'nom_région',
#  'chef-lieu_région',
#  'numéro_département',
#  'nom_département',
#  'préfecture',
#  'numéro_circonscription',
#  'nom_commune',
#  'codes_postaux',
#  'code_insee',
#  'latitude',
#  'longitude',
#  'éloignement']
