# Generated by Django 2.2 on 2019-05-28 10:03

from django.db import migrations


def load_data(apps, schema_editor):
    Energy = apps.get_model("energies", "Energy")
    energies = Energy.objects.all()

    for energy in energies:
        if energy.pk == 5:
            energy.combustible_category = "electricity"
            energy.save()
        elif energy.pk in [6, 7, 8, 9, 10]:
            energy.combustible_category = "renewable"
            energy.save()


class Migration(migrations.Migration):

    dependencies = [
        ('energies', '0012_energy_combustible_category'),
    ]

    operations = [
        migrations.RunPython(load_data, reverse_code=migrations.RunPython.noop),
    ]
