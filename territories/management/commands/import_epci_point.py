from django.core.management.base import BaseCommand
from config import settings
from territories.models import Epci
import json


class Command(BaseCommand):

    help = "Import geojson points des epci"

    def handle(self, *args, **options):

        path = settings.BASE_DIR + "/territories/shapefile/EPCI_POINT.geojson"
        with open(path) as json_data:
            data_dict = json.load(json_data)

        for feature in data_dict["features"]:
            epci = Epci.objects.get(inseecode=feature["properties"]["CODE_EPCI"])
            epci.geom = feature["geometry"]
            epci.save()


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
