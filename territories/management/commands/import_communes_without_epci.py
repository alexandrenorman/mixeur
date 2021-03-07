from django.db import transaction
from django.core.management.base import BaseCommand
from config import settings
from territories.models import Commune, Departement, Epci
import shapefile


class Command(BaseCommand):

    help = "Import shapefile des territoires"

    def handle(self, *args, **options):
        path = settings.BASE_DIR + "/territories/shapefile/COMMUNE.shp"
        print(path)

        reader = shapefile.Reader(path, encoding="latin1")
        with transaction.atomic():
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
                        defaults={
                            "name": name,
                            "departement": departement,
                            "epci": epci,
                        },
                    )
                except Exception as e:
                    print(
                        f"ERROR {inseecode} : {name} - {row[6]} - EPCI {row[9]}\n{e.args}"
                    )
