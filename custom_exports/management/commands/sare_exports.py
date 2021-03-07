"""
Ce script permet de générer les exports pour le programme SARE

Pour le lancer :

    inv run -c "sare_exports"

"""
import os
import sys

from django.core.management.base import BaseCommand

from custom_exports.exports import ExportSare
from custom_exports.helpers import DataAdapter, DataExporter

from helpers.strings import print_boxed


class Command(BaseCommand):
    help = "Create exports for SARE"  # NOQA: A003

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("output", type=str)

        parser.add_argument(
            "--export",
            help="Export type [csv], [xlsx] or [sare]",
        )

        parser.add_argument(
            "--group-pk",
            help="Group PK to export",
        )

    def handle(self, *args, **options):

        filename = os.path.join("/app/exports", options["output"])

        mode = options["export"]
        if mode is None:
            mode = "csv"
        elif mode not in ["csv", "xlsx", "sare"]:
            print_boxed(f"ERROR: Format {mode} unknown.")
            sys.exit(1)

        group_pk = options["group_pk"]

        print_boxed(
            f"Starting export for SARE in {filename} [mode: {mode}] for group {group_pk}"
        )

        es = ExportSare(group_pk=group_pk)

        da = DataAdapter(
            adapters=es.adapters(),
        )

        de = DataExporter(
            rows=es.objects(),
            columns=es.columns(),
            data_adapter=da,
        )

        if mode == "csv":
            csv = de.export_as_csv()
            with open(filename, "w", encoding="utf-8") as output:
                output.write(csv)

        if mode == "sare":
            csv = de.export_as_sare()
            with open(filename, "wb") as output:
                output.write(csv)

        elif mode == "xlsx":
            xls = de.export_as_excel()
            with open(filename, "wb") as output:
                output.write(xls)

        print_boxed(f"Export for SARE done in {filename}")
