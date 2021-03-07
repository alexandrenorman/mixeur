# Generated by Django 2.1.5 on 2019-02-26 15:10

import json
from django.db import migrations


def load_fixture(apps, schema_editor):
    Energy = apps.get_model("energies", "Energy")
    with open('./energies/fixtures/energy_data.json') as json_file:
        data = json.load(json_file)
        energy_records = []
        for entry in data:
            fields = entry['fields']
            energy_records.append(Energy(
                identifier=fields['identifier'],
                primary_energy_ratio=fields['primary_energy_ratio'],
                ghg_ratio=fields['ghg_ratio'],
                carbon_tax=fields['carbon_tax'],
                pci_ratio=fields['pci_ratio'],
                density_ratio=fields['density_ratio'],
            ))
    Energy.objects.bulk_create(energy_records)

    YearlyEnergyPrice = apps.get_model("energies", "YearlyEnergyPrice")
    with open('./energies/fixtures/yearly_energy_price_data.json') as json_file:
        data = json.load(json_file)
        yearly_energy_price_records = []
        for entry in data:
            fields = entry['fields']
            yearly_energy_price_records.append(YearlyEnergyPrice(
                year=fields['year'],
                energy=Energy.objects.get(pk=fields['energy']),
                price=fields['price'],
            ))
    YearlyEnergyPrice.objects.bulk_create(yearly_energy_price_records)


def unload_fixture(apps, schema_editor):
    energy_model = apps.get_model("energies", "Energy")
    energy_model.objects.all().delete()
    yearly_energy_price_model = apps.get_model("energies", "YearlyEnergyPrice")
    yearly_energy_price_model.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('energies', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture, reverse_code=unload_fixture),
    ]
