# Generated by Django 2.2.3 on 2019-08-23 07:54

from django.db import migrations
from decimal import Decimal


def update_energy_price_variations(apps, schema_editor):
    Energy = apps.get_model("energies", "Energy")

    energy_price_variations = {
        "oil": Decimal("0.0346"),
        "propane": Decimal("0.0295"),
        "gaz_b1": Decimal("0.0132"),
        "electricity": Decimal("0.0280"),
        "bulk_granules": Decimal("0.0312"),
        "bag_granules": Decimal("0.0312"),
        "wood": Decimal("0.0273"),
        "shredded_wood": Decimal("0.0206"),
        "network": Decimal("0.0200"),
    }

    for identifier, price_variation in energy_price_variations.items():
        Energy.objects.filter(identifier=identifier).update(
            price_variation=price_variation
        )


class Migration(migrations.Migration):

    dependencies = [("energies", "0028_update_energy_price_variation")]

    operations = [
        migrations.RunPython(
            update_energy_price_variations, reverse_code=migrations.RunPython.noop
        )
    ]
