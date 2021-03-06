# Generated by Django 2.2.3 on 2019-07-05 16:24

from django.db import migrations


def load_data(apps, schema_editor):

    variations = {
        "oil": 0.047,
        "gaz_b0": 0.0373,
        "gaz_b1": 0.0373,
        "propane": 0.0378,
        "electricity": 0.0302,
        "wood": 0.0274,
        "shredded_wood": 0.0296,
        "bulk_granules": 0.0378,
        "bag_granules": 0.0378,
        "network": 0.02,
    }

    Energy = apps.get_model("energies", "Energy")

    for energy in Energy.objects.all():
        energy.price_variation = variations[energy.identifier]
        energy.save()


class Migration(migrations.Migration):

    dependencies = [("energies", "0019_energy_price_variation")]

    operations = [
        migrations.RunPython(load_data, reverse_code=migrations.RunPython.noop)
    ]

