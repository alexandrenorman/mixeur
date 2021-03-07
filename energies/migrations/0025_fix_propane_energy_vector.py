# Generated by Django 2.2.3 on 2019-08-21 09:07

from django.db import migrations


def fix_propane_energy(apps, schema_editor):
    EnergyVector = apps.get_model("energies", "EnergyVector")
    Energy = apps.get_model("energies", "Energy")

    propane = Energy.objects.get(identifier="propane")

    EnergyVector.objects.filter(vector__in=("propane_kg", "propane_m3")).update(
        energy=propane
    )


class Migration(migrations.Migration):

    dependencies = [("energies", "0024_fix_pci_decimal_resolution")]

    operations = [
        migrations.RunPython(fix_propane_energy, reverse_code=migrations.RunPython.noop)
    ]

