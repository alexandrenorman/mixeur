# Generated by Django 2.2.10 on 2020-05-05 12:08

from django.db import migrations, models


def load_data(apps, schema_editor):
    BuildingHeatingConsumption = apps.get_model("energies", "BuildingHeatingConsumption")
    # Delete all existing building heating consumptions
    # (only thermix use it for now. + no manual modification)
    BuildingHeatingConsumption.objects.all().delete()

    BuildingHeatingConsumption.objects.bulk_create([
        BuildingHeatingConsumption(criterion="before_1919", heating_consumption=170, comment="", order=10),
        BuildingHeatingConsumption(criterion="between_1919_1945", heating_consumption=190, comment="", order=20),
        BuildingHeatingConsumption(criterion="between_1946_1970", heating_consumption=170, comment="", order=30),
        BuildingHeatingConsumption(criterion="between_1971_1990", heating_consumption=136, comment="", order=40),
        BuildingHeatingConsumption(criterion="between_1991_2005", heating_consumption=117, comment="", order=50),
        BuildingHeatingConsumption(criterion="between_2006_2012", heating_consumption=94, comment="RT 2005", order=60),
        BuildingHeatingConsumption(criterion="after_2012", heating_consumption=32, comment="RT 2012", order=70),
        BuildingHeatingConsumption(criterion="bbc", heating_consumption=60, comment="Label BBC", order=80),
        BuildingHeatingConsumption(criterion="passive", heating_consumption=15, comment="Label Passiv Haus", order=90),
    ])

    
class Migration(migrations.Migration):

    dependencies = [
        ('energies', '0003_2019_energy_prices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingheatingconsumption',
            name='criterion',
            field=models.CharField(choices=[('before_1919', 'Avant 1919'), ('between_1919_1945', 'Entre 1919 et 1945'), ('between_1946_1970', 'Entre 1946 et 1970'), ('between_1971_1990', 'Entre 1971 et 1990'), ('between_1991_2005', 'Entre 1991 et 2005'), ('between_2006_2012', 'Entre 2006 et 2012'), ('after_2012', 'Après 2012'), ('bbc', 'Bâtiment rénové au niveau basse consommation (BBC)'), ('passive', 'Bâtiment rénové au niveau passif')], max_length=30, unique=True, verbose_name='Critère'),
        ),
        migrations.RunPython(load_data, reverse_code=migrations.RunPython.noop),

    ]

