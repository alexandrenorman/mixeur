from django.core.management.base import BaseCommand
from config import settings
from territories.models import Commune

from django.db import transaction


class Command(BaseCommand):

    help = "Import shapefile des territoires"

    def handle(self, *args, **options):

        path = settings.BASE_DIR + "/territories/shapefile/laposte_hexasmal.csv"
        print(path)

        with transaction.atomic():
            for line in open(path, "r").readlines()[1:]:
                # Code_commune_INSEE;Nom_commune;Code_postal;Libelle_acheminement;Ligne_5;coordonnees_gps
                inseecode, name, postcode, o1, o2, o3 = line.split(";")

                if Commune.objects.filter(inseecode=inseecode).exists():
                    c = Commune.objects.get(inseecode=inseecode)
                    c.postcode = postcode
                    c.save()
                else:
                    print(line)
