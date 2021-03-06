# Generated by Django 2.2.10 on 2020-08-20 14:28

from django.db import migrations


def fix_solar_system_combined_maintenance_price(apps, schema_editor):
    ProductionSystem = apps.get_model("energies", "ProductionSystem")

    solar_system_combined = ProductionSystem.objects.get(
        identifier="solar_system_combined"
    )
    solar_system_combined.maintenance_individual_heating = 25
    solar_system_combined.maintenance_individual_hot_water = 25
    solar_system_combined.maintenance_small_multi_unit_heating = 15
    solar_system_combined.maintenance_medium_multi_unit_heating = 15
    solar_system_combined.maintenance_large_multi_unit_heating = 15
    solar_system_combined.maintenance_small_multi_unit_hot_water = 15
    solar_system_combined.maintenance_medium_multi_unit_hot_water = 15
    solar_system_combined.maintenance_large_multi_unit_hot_water = 15
    solar_system_combined.save()


def unfix_solar_system_combined_maintenance_price(apps, schema_editor):
    ProductionSystem = apps.get_model("energies", "ProductionSystem")

    solar_system_combined = ProductionSystem.objects.get(
        identifier="solar_system_combined"
    )
    solar_system_combined.maintenance_individual_heating = 50
    solar_system_combined.maintenance_individual_hot_water = 50
    solar_system_combined.maintenance_small_multi_unit_heating = 30
    solar_system_combined.maintenance_medium_multi_unit_heating = 30
    solar_system_combined.maintenance_large_multi_unit_heating = 30
    solar_system_combined.maintenance_small_multi_unit_hot_water = 30
    solar_system_combined.maintenance_medium_multi_unit_hot_water = 30
    solar_system_combined.maintenance_large_multi_unit_hot_water = 30
    solar_system_combined.save()


class Migration(migrations.Migration):

    dependencies = [
        ("energies", "0006_new_logs_based_production_systems_data"),
    ]

    operations = [
        migrations.RunPython(
            fix_solar_system_combined_maintenance_price,
            reverse_code=unfix_solar_system_combined_maintenance_price,
        ),
    ]
