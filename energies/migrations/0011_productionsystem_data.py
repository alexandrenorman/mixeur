# Generated by Django 2.2 on 2019-05-07 09:34

from decimal import Decimal
from django.db import migrations


def load_data(apps, schema_editor):
    ProductionSystem = apps.get_model("energies", "ProductionSystem")
    Energy = apps.get_model("energies", "Energy")

    energies = {vector.identifier: vector for vector in Energy.objects.all()}

    ProductionSystem.objects.bulk_create([
        ProductionSystem(identifier="oil_boiler_standard", is_heating=True, is_hot_water=True, is_individual=True, is_multi_unit=True, efficiency_heating=Decimal("0.82"), efficiency_hot_water=Decimal("0.58"), energy=energies["oil"], is_hydro=True, enr_ratio_heating=Decimal("0"), enr_ratio_hot_water=Decimal("0"), investment_individual_heating="5000", investment_individual_hot_water="5000", investment_small_multi_unit_heating="20000", investment_medium_multi_unit_heating="35000", investment_large_multi_unit_heating="45000", investment_small_multi_unit_hot_water="26000", investment_medium_multi_unit_hot_water="45500", investment_large_multi_unit_hot_water="60000", maintenance_individual_heating="150", maintenance_individual_hot_water="150", maintenance_small_multi_unit_heating="1500", maintenance_medium_multi_unit_heating="3000", maintenance_large_multi_unit_heating="6000", maintenance_small_multi_unit_hot_water="3200", maintenance_medium_multi_unit_hot_water="6000", maintenance_large_multi_unit_hot_water="7800", provisions_small_multi_unit_heating="600", provisions_medium_multi_unit_heating="1050", provisions_large_multi_unit_heating="1350", provisions_small_multi_unit_hot_water="780", provisions_medium_multi_unit_hot_water="1365", provisions_large_multi_unit_hot_water="1800"),
        ProductionSystem(identifier="oil_boiler_condensing", is_heating=True, is_hot_water=True, is_individual=True, is_multi_unit=True, efficiency_heating=Decimal("0.93"), efficiency_hot_water=Decimal("0.6"), energy=energies["oil"], is_hydro=True, enr_ratio_heating=Decimal("0"), enr_ratio_hot_water=Decimal("0"), investment_individual_heating="6000", investment_individual_hot_water="6000", investment_small_multi_unit_heating="22000", investment_medium_multi_unit_heating="38000", investment_large_multi_unit_heating="50000", investment_small_multi_unit_hot_water="28000", investment_medium_multi_unit_hot_water="50000", investment_large_multi_unit_hot_water="65000", maintenance_individual_heating="150", maintenance_individual_hot_water="150", maintenance_small_multi_unit_heating="1500", maintenance_medium_multi_unit_heating="3000", maintenance_large_multi_unit_heating="6000", maintenance_small_multi_unit_hot_water="3200", maintenance_medium_multi_unit_hot_water="6000", maintenance_large_multi_unit_hot_water="7800", provisions_small_multi_unit_heating="660", provisions_medium_multi_unit_heating="1140", provisions_large_multi_unit_heating="1500", provisions_small_multi_unit_hot_water="840", provisions_medium_multi_unit_hot_water="1500", provisions_large_multi_unit_hot_water="1950"),
        ProductionSystem(identifier="gaz_boiler_standard", is_heating=True, is_hot_water=True, is_individual=True, is_multi_unit=True, efficiency_heating=Decimal("0.82"), efficiency_hot_water=Decimal("0.62"), energy=energies["gaz_b1"], is_hydro=True, enr_ratio_heating=Decimal("0"), enr_ratio_hot_water=Decimal("0"), investment_individual_heating="4000", investment_individual_hot_water="4000", investment_small_multi_unit_heating="15000", investment_medium_multi_unit_heating="30000", investment_large_multi_unit_heating="40000", investment_small_multi_unit_hot_water="20000", investment_medium_multi_unit_hot_water="40000", investment_large_multi_unit_hot_water="52000", maintenance_individual_heating="150", maintenance_individual_hot_water="150", maintenance_small_multi_unit_heating="1000", maintenance_medium_multi_unit_heating="2000", maintenance_large_multi_unit_heating="5000", maintenance_small_multi_unit_hot_water="1000", maintenance_medium_multi_unit_hot_water="2000", maintenance_large_multi_unit_hot_water="5000", provisions_small_multi_unit_heating="450", provisions_medium_multi_unit_heating="900", provisions_large_multi_unit_heating="1200", provisions_small_multi_unit_hot_water="600", provisions_medium_multi_unit_hot_water="1200", provisions_large_multi_unit_hot_water="1560"),
        ProductionSystem(identifier="gaz_boiler_condensing", is_heating=True, is_hot_water=True, is_individual=True, is_multi_unit=True, efficiency_heating=Decimal("0.95"), efficiency_hot_water=Decimal("0.72"), energy=energies["gaz_b1"], is_hydro=True, enr_ratio_heating=Decimal("0"), enr_ratio_hot_water=Decimal("0"), investment_individual_heating="5000", investment_individual_hot_water="5000", investment_small_multi_unit_heating="17000", investment_medium_multi_unit_heating="33000", investment_large_multi_unit_heating="45000", investment_small_multi_unit_hot_water="22000", investment_medium_multi_unit_hot_water="43000", investment_large_multi_unit_hot_water="60000", maintenance_individual_heating="150", maintenance_individual_hot_water="150", maintenance_small_multi_unit_heating="1000", maintenance_medium_multi_unit_heating="2000", maintenance_large_multi_unit_heating="5000", maintenance_small_multi_unit_hot_water="1000", maintenance_medium_multi_unit_hot_water="2000", maintenance_large_multi_unit_hot_water="5000", provisions_small_multi_unit_heating="510", provisions_medium_multi_unit_heating="990", provisions_large_multi_unit_heating="1350", provisions_small_multi_unit_hot_water="660", provisions_medium_multi_unit_hot_water="1290", provisions_large_multi_unit_hot_water="1800"),
        ProductionSystem(identifier="propane_boiler_standard", is_heating=True, is_hot_water=True, is_individual=True, is_multi_unit=True, efficiency_heating=Decimal("0.82"), efficiency_hot_water=Decimal("0.62"), energy=energies["propane"], is_hydro=True, enr_ratio_heating=Decimal("0"), enr_ratio_hot_water=Decimal("0"), investment_individual_heating="5000", investment_individual_hot_water="5000", investment_small_multi_unit_heating="20000", investment_medium_multi_unit_heating="35000", investment_large_multi_unit_heating="45000", investment_small_multi_unit_hot_water="26000", investment_medium_multi_unit_hot_water="45000", investment_large_multi_unit_hot_water="60000", maintenance_individual_heating="150", maintenance_individual_hot_water="150", maintenance_small_multi_unit_heating="1500", maintenance_medium_multi_unit_heating="3000", maintenance_large_multi_unit_heating="6000", maintenance_small_multi_unit_hot_water="3200", maintenance_medium_multi_unit_hot_water="6000", maintenance_large_multi_unit_hot_water="7800", provisions_small_multi_unit_heating="600", provisions_medium_multi_unit_heating="1050", provisions_large_multi_unit_heating="1350", provisions_small_multi_unit_hot_water="780", provisions_medium_multi_unit_hot_water="1350", provisions_large_multi_unit_hot_water="1800"),
        ProductionSystem(identifier="propane_boiler_condensing", is_heating=True, is_hot_water=True, is_individual=True, is_multi_unit=True, efficiency_heating=Decimal("0.95"), efficiency_hot_water=Decimal("0.72"), energy=energies["propane"], is_hydro=True, enr_ratio_heating=Decimal("0"), enr_ratio_hot_water=Decimal("0"), investment_individual_heating="6000", investment_individual_hot_water="6000", investment_small_multi_unit_heating="22000", investment_medium_multi_unit_heating="38000", investment_large_multi_unit_heating="50000", investment_small_multi_unit_hot_water="28000", investment_medium_multi_unit_hot_water="50000", investment_large_multi_unit_hot_water="65000", maintenance_individual_heating="150", maintenance_individual_hot_water="150", maintenance_small_multi_unit_heating="1500", maintenance_medium_multi_unit_heating="3000", maintenance_large_multi_unit_heating="6000", maintenance_small_multi_unit_hot_water="3200", maintenance_medium_multi_unit_hot_water="6000", maintenance_large_multi_unit_hot_water="7800", provisions_small_multi_unit_heating="660", provisions_medium_multi_unit_heating="1140", provisions_large_multi_unit_heating="1500", provisions_small_multi_unit_hot_water="840", provisions_medium_multi_unit_hot_water="1500", provisions_large_multi_unit_hot_water="1950"),
        ProductionSystem(identifier="electric_boiler", is_heating=True, is_hot_water=True, is_individual=True, is_multi_unit=True, efficiency_heating=Decimal("1"), efficiency_hot_water=Decimal("0.95"), energy=energies["electricity"], is_hydro=True, enr_ratio_heating=Decimal("0"), enr_ratio_hot_water=Decimal("0"), investment_individual_heating="3000", investment_individual_hot_water="3500", investment_small_multi_unit_heating="10000", investment_medium_multi_unit_heating="20000", investment_large_multi_unit_heating="30000", investment_small_multi_unit_hot_water="13000", investment_medium_multi_unit_hot_water="26000", investment_large_multi_unit_hot_water="40000", maintenance_individual_heating="150", maintenance_individual_hot_water="150", maintenance_small_multi_unit_heating="1000", maintenance_medium_multi_unit_heating="2000", maintenance_large_multi_unit_heating="5000", maintenance_small_multi_unit_hot_water="1000", maintenance_medium_multi_unit_hot_water="2000", maintenance_large_multi_unit_hot_water="5000", provisions_small_multi_unit_heating="300", provisions_medium_multi_unit_heating="600", provisions_large_multi_unit_heating="900", provisions_small_multi_unit_hot_water="390", provisions_medium_multi_unit_hot_water="780", provisions_large_multi_unit_hot_water="1200"),
        ProductionSystem(identifier="electric_radiators", is_heating=True, is_hot_water=False, is_individual=True, is_multi_unit=False, efficiency_heating=Decimal("1"), efficiency_hot_water=None, energy=energies["electricity"], is_hydro=False, enr_ratio_heating=Decimal("0"), enr_ratio_hot_water=None, investment_individual_heating="3000", investment_individual_hot_water=None, investment_small_multi_unit_heating=None, investment_medium_multi_unit_heating=None, investment_large_multi_unit_heating=None, investment_small_multi_unit_hot_water=None, investment_medium_multi_unit_hot_water=None, investment_large_multi_unit_hot_water=None, maintenance_individual_heating="0", maintenance_individual_hot_water=None, maintenance_small_multi_unit_heating=None, maintenance_medium_multi_unit_heating=None, maintenance_large_multi_unit_heating=None, maintenance_small_multi_unit_hot_water=None, maintenance_medium_multi_unit_hot_water=None, maintenance_large_multi_unit_hot_water=None, provisions_small_multi_unit_heating=None, provisions_medium_multi_unit_heating=None, provisions_large_multi_unit_heating=None, provisions_small_multi_unit_hot_water=None, provisions_medium_multi_unit_hot_water=None, provisions_large_multi_unit_hot_water=None),
        ProductionSystem(identifier="heat_pump_air_air", is_heating=True, is_hot_water=False, is_individual=True, is_multi_unit=False, efficiency_heating=Decimal("1.87"), efficiency_hot_water=None, energy=energies["electricity"], is_hydro=False, enr_ratio_heating=Decimal("0"), enr_ratio_hot_water=None, investment_individual_heating="6000", investment_individual_hot_water=None, investment_small_multi_unit_heating=None, investment_medium_multi_unit_heating=None, investment_large_multi_unit_heating=None, investment_small_multi_unit_hot_water=None, investment_medium_multi_unit_hot_water=None, investment_large_multi_unit_hot_water=None, maintenance_individual_heating="200", maintenance_individual_hot_water=None, maintenance_small_multi_unit_heating=None, maintenance_medium_multi_unit_heating=None, maintenance_large_multi_unit_heating=None, maintenance_small_multi_unit_hot_water=None, maintenance_medium_multi_unit_hot_water=None, maintenance_large_multi_unit_hot_water=None, provisions_small_multi_unit_heating=None, provisions_medium_multi_unit_heating=None, provisions_large_multi_unit_heating=None, provisions_small_multi_unit_hot_water=None, provisions_medium_multi_unit_hot_water=None, provisions_large_multi_unit_hot_water=None),
        ProductionSystem(identifier="heat_pump_air_water", is_heating=True, is_hot_water=True, is_individual=True, is_multi_unit=False, efficiency_heating=Decimal("2.2"), efficiency_hot_water=Decimal("1.32"), energy=energies["electricity"], is_hydro=True, enr_ratio_heating=Decimal("0"), enr_ratio_hot_water=Decimal("0"), investment_individual_heating="12000", investment_individual_hot_water="12000", investment_small_multi_unit_heating=None, investment_medium_multi_unit_heating=None, investment_large_multi_unit_heating=None, investment_small_multi_unit_hot_water=None, investment_medium_multi_unit_hot_water=None, investment_large_multi_unit_hot_water=None, maintenance_individual_heating="200", maintenance_individual_hot_water="200", maintenance_small_multi_unit_heating=None, maintenance_medium_multi_unit_heating=None, maintenance_large_multi_unit_heating=None, maintenance_small_multi_unit_hot_water=None, maintenance_medium_multi_unit_hot_water=None, maintenance_large_multi_unit_hot_water=None, provisions_small_multi_unit_heating=None, provisions_medium_multi_unit_heating=None, provisions_large_multi_unit_heating=None, provisions_small_multi_unit_hot_water=None, provisions_medium_multi_unit_hot_water=None, provisions_large_multi_unit_hot_water=None),
        ProductionSystem(identifier="heat_pump_geothermal_lte", is_heating=True, is_hot_water=True, is_individual=True, is_multi_unit=True, efficiency_heating=Decimal("3.4"), efficiency_hot_water=Decimal("2.04"), energy=energies["electricity"], is_hydro=True, enr_ratio_heating=Decimal("0.241176470588235"), enr_ratio_hot_water=Decimal("0"), investment_individual_heating="20000", investment_individual_hot_water="20000", investment_small_multi_unit_heating="80000", investment_medium_multi_unit_heating="150000", investment_large_multi_unit_heating="250000", investment_small_multi_unit_hot_water="100000", investment_medium_multi_unit_hot_water="200000", investment_large_multi_unit_hot_water="300000", maintenance_individual_heating="200", maintenance_individual_hot_water="200", maintenance_small_multi_unit_heating="1500", maintenance_medium_multi_unit_heating="3000", maintenance_large_multi_unit_heating="6000", maintenance_small_multi_unit_hot_water="2000", maintenance_medium_multi_unit_hot_water="4000", maintenance_large_multi_unit_hot_water="8000", provisions_small_multi_unit_heating="2400", provisions_medium_multi_unit_heating="4500", provisions_large_multi_unit_heating="7500", provisions_small_multi_unit_hot_water="3000", provisions_medium_multi_unit_hot_water="6000", provisions_large_multi_unit_hot_water="9000"),
        ProductionSystem(identifier="heat_pump_geothermal_vlte", is_heating=True, is_hot_water=True, is_individual=True, is_multi_unit=True, efficiency_heating=Decimal("3.8"), efficiency_hot_water=Decimal("2.28"), energy=energies["electricity"], is_hydro=True, enr_ratio_heating=Decimal("0.321052631578947"), enr_ratio_hot_water=Decimal("0"), investment_individual_heating="20000", investment_individual_hot_water="20000", investment_small_multi_unit_heating="80000", investment_medium_multi_unit_heating="150000", investment_large_multi_unit_heating="250000", investment_small_multi_unit_hot_water="100000", investment_medium_multi_unit_hot_water="200000", investment_large_multi_unit_hot_water="300000", maintenance_individual_heating="200", maintenance_individual_hot_water="200", maintenance_small_multi_unit_heating="1500", maintenance_medium_multi_unit_heating="3000", maintenance_large_multi_unit_heating="6000", maintenance_small_multi_unit_hot_water="2000", maintenance_medium_multi_unit_hot_water="4000", maintenance_large_multi_unit_hot_water="8000", provisions_small_multi_unit_heating="2400", provisions_medium_multi_unit_heating="4500", provisions_large_multi_unit_heating="7500", provisions_small_multi_unit_hot_water="3000", provisions_medium_multi_unit_hot_water="6000", provisions_large_multi_unit_hot_water="9000"),
        ProductionSystem(identifier="thermodynamic_cmv", is_heating=True, is_hot_water=True, is_individual=True, is_multi_unit=False, efficiency_heating=Decimal("5.2"), efficiency_hot_water=Decimal("3.12"), energy=energies["electricity"], is_hydro=True, enr_ratio_heating=Decimal("0.503846153846154"), enr_ratio_hot_water=Decimal("0.173076923076923"), investment_individual_heating="15000", investment_individual_hot_water="15000", investment_small_multi_unit_heating=None, investment_medium_multi_unit_heating=None, investment_large_multi_unit_heating=None, investment_small_multi_unit_hot_water=None, investment_medium_multi_unit_hot_water=None, investment_large_multi_unit_hot_water=None, maintenance_individual_heating="200", maintenance_individual_hot_water="200", maintenance_small_multi_unit_heating=None, maintenance_medium_multi_unit_heating=None, maintenance_large_multi_unit_heating=None, maintenance_small_multi_unit_hot_water=None, maintenance_medium_multi_unit_hot_water=None, maintenance_large_multi_unit_hot_water=None, provisions_small_multi_unit_heating=None, provisions_medium_multi_unit_heating=None, provisions_large_multi_unit_heating=None, provisions_small_multi_unit_hot_water=None, provisions_medium_multi_unit_hot_water=None, provisions_large_multi_unit_hot_water=None),
        ProductionSystem(identifier="log_stove", is_heating=True, is_hot_water=False, is_individual=True, is_multi_unit=False, efficiency_heating=Decimal("0.7"), efficiency_hot_water=None, energy=energies["wood"], is_hydro=False, enr_ratio_heating=Decimal("1"), enr_ratio_hot_water=None, investment_individual_heating="3000", investment_individual_hot_water=None, investment_small_multi_unit_heating=None, investment_medium_multi_unit_heating=None, investment_large_multi_unit_heating=None, investment_small_multi_unit_hot_water=None, investment_medium_multi_unit_hot_water=None, investment_large_multi_unit_hot_water=None, maintenance_individual_heating="80", maintenance_individual_hot_water=None, maintenance_small_multi_unit_heating=None, maintenance_medium_multi_unit_heating=None, maintenance_large_multi_unit_heating=None, maintenance_small_multi_unit_hot_water=None, maintenance_medium_multi_unit_hot_water=None, maintenance_large_multi_unit_hot_water=None, provisions_small_multi_unit_heating=None, provisions_medium_multi_unit_heating=None, provisions_large_multi_unit_heating=None, provisions_small_multi_unit_hot_water=None, provisions_medium_multi_unit_hot_water=None, provisions_large_multi_unit_hot_water=None),
        ProductionSystem(identifier="granulated_wood_stove", is_heating=True, is_hot_water=False, is_individual=True, is_multi_unit=False, efficiency_heating=Decimal("0.8"), efficiency_hot_water=None, energy=energies["bag_granules"], is_hydro=False, enr_ratio_heating=Decimal("1"), enr_ratio_hot_water=None, investment_individual_heating="5000", investment_individual_hot_water=None, investment_small_multi_unit_heating=None, investment_medium_multi_unit_heating=None, investment_large_multi_unit_heating=None, investment_small_multi_unit_hot_water=None, investment_medium_multi_unit_hot_water=None, investment_large_multi_unit_hot_water=None, maintenance_individual_heating="100", maintenance_individual_hot_water=None, maintenance_small_multi_unit_heating=None, maintenance_medium_multi_unit_heating=None, maintenance_large_multi_unit_heating=None, maintenance_small_multi_unit_hot_water=None, maintenance_medium_multi_unit_hot_water=None, maintenance_large_multi_unit_hot_water=None, provisions_small_multi_unit_heating=None, provisions_medium_multi_unit_heating=None, provisions_large_multi_unit_heating=None, provisions_small_multi_unit_hot_water=None, provisions_medium_multi_unit_hot_water=None, provisions_large_multi_unit_hot_water=None),
        ProductionSystem(identifier="granulated_wood_boiler", is_heating=True, is_hot_water=True, is_individual=True, is_multi_unit=True, efficiency_heating=Decimal("0.85"), efficiency_hot_water=Decimal("0.72"), energy=energies["bulk_granules"], is_hydro=True, enr_ratio_heating=Decimal("1"), enr_ratio_hot_water=Decimal("1"), investment_individual_heating="16000", investment_individual_hot_water="16000", investment_small_multi_unit_heating="60000", investment_medium_multi_unit_heating="110000", investment_large_multi_unit_heating="180000", investment_small_multi_unit_hot_water="80000", investment_medium_multi_unit_hot_water="140000", investment_large_multi_unit_hot_water="230000", maintenance_individual_heating="250", maintenance_individual_hot_water="250", maintenance_small_multi_unit_heating="3000", maintenance_medium_multi_unit_heating="6000", maintenance_large_multi_unit_heating="12000", maintenance_small_multi_unit_hot_water="4000", maintenance_medium_multi_unit_hot_water="7000", maintenance_large_multi_unit_hot_water="15000", provisions_small_multi_unit_heating="1800", provisions_medium_multi_unit_heating="3300", provisions_large_multi_unit_heating="5400", provisions_small_multi_unit_hot_water="2400", provisions_medium_multi_unit_hot_water="4200", provisions_large_multi_unit_hot_water="6900"),
        ProductionSystem(identifier="log_boiler", is_heating=True, is_hot_water=True, is_individual=True, is_multi_unit=False, efficiency_heating=Decimal("0.72"), efficiency_hot_water=Decimal("0.65"), energy=energies["wood"], is_hydro=True, enr_ratio_heating=Decimal("1"), enr_ratio_hot_water=Decimal("1"), investment_individual_heating="12000", investment_individual_hot_water="12000", investment_small_multi_unit_heating=None, investment_medium_multi_unit_heating=None, investment_large_multi_unit_heating=None, investment_small_multi_unit_hot_water=None, investment_medium_multi_unit_hot_water=None, investment_large_multi_unit_hot_water=None, maintenance_individual_heating="200", maintenance_individual_hot_water="200", maintenance_small_multi_unit_heating=None, maintenance_medium_multi_unit_heating=None, maintenance_large_multi_unit_heating=None, maintenance_small_multi_unit_hot_water=None, maintenance_medium_multi_unit_hot_water=None, maintenance_large_multi_unit_hot_water=None, provisions_small_multi_unit_heating=None, provisions_medium_multi_unit_heating=None, provisions_large_multi_unit_heating=None, provisions_small_multi_unit_hot_water=None, provisions_medium_multi_unit_hot_water=None, provisions_large_multi_unit_hot_water=None),
        ProductionSystem(identifier="shredded_wood_boiler", is_heating=True, is_hot_water=True, is_individual=True, is_multi_unit=True, efficiency_heating=Decimal("0.8"), efficiency_hot_water=Decimal("0.68"), energy=energies["shredded_wood"], is_hydro=True, enr_ratio_heating=Decimal("1"), enr_ratio_hot_water=Decimal("1"), investment_individual_heating="25000", investment_individual_hot_water="25000", investment_small_multi_unit_heating="150000", investment_medium_multi_unit_heating="300000", investment_large_multi_unit_heating="450000", investment_small_multi_unit_hot_water="200000", investment_medium_multi_unit_hot_water="400000", investment_large_multi_unit_hot_water="550000", maintenance_individual_heating="400", maintenance_individual_hot_water="400", maintenance_small_multi_unit_heating="3000", maintenance_medium_multi_unit_heating="4500", maintenance_large_multi_unit_heating="15000", maintenance_small_multi_unit_hot_water="3000", maintenance_medium_multi_unit_hot_water="4500", maintenance_large_multi_unit_hot_water="15000", provisions_small_multi_unit_heating="4500", provisions_medium_multi_unit_heating="9000", provisions_large_multi_unit_heating="13500", provisions_small_multi_unit_hot_water="6000", provisions_medium_multi_unit_hot_water="12000", provisions_large_multi_unit_hot_water="16500"),
        ProductionSystem(identifier="recent_log_boiler_stove", is_heating=False, is_hot_water=True, is_individual=True, is_multi_unit=False, efficiency_heating=None, efficiency_hot_water=Decimal("0.58"), energy=energies["wood"], is_hydro=False, enr_ratio_heating=None, enr_ratio_hot_water=Decimal("0"), investment_individual_heating=None, investment_individual_hot_water="3000", investment_small_multi_unit_heating=None, investment_medium_multi_unit_heating=None, investment_large_multi_unit_heating=None, investment_small_multi_unit_hot_water=None, investment_medium_multi_unit_hot_water=None, investment_large_multi_unit_hot_water=None, maintenance_individual_heating=None, maintenance_individual_hot_water="80", maintenance_small_multi_unit_heating=None, maintenance_medium_multi_unit_heating=None, maintenance_large_multi_unit_heating=None, maintenance_small_multi_unit_hot_water=None, maintenance_medium_multi_unit_hot_water=None, maintenance_large_multi_unit_hot_water=None, provisions_small_multi_unit_heating=None, provisions_medium_multi_unit_heating=None, provisions_large_multi_unit_heating=None, provisions_small_multi_unit_hot_water=None, provisions_medium_multi_unit_hot_water=None, provisions_large_multi_unit_hot_water=None),
        ProductionSystem(identifier="granulated_wood_boiler_stove", is_heating=False, is_hot_water=True, is_individual=True, is_multi_unit=False, efficiency_heating=None, efficiency_hot_water=Decimal("0.68"), energy=energies["bag_granules"], is_hydro=False, enr_ratio_heating=None, enr_ratio_hot_water=Decimal("0"), investment_individual_heating=None, investment_individual_hot_water="5000", investment_small_multi_unit_heating=None, investment_medium_multi_unit_heating=None, investment_large_multi_unit_heating=None, investment_small_multi_unit_hot_water=None, investment_medium_multi_unit_hot_water=None, investment_large_multi_unit_hot_water=None, maintenance_individual_heating=None, maintenance_individual_hot_water="100", maintenance_small_multi_unit_heating=None, maintenance_medium_multi_unit_heating=None, maintenance_large_multi_unit_heating=None, maintenance_small_multi_unit_hot_water=None, maintenance_medium_multi_unit_hot_water=None, maintenance_large_multi_unit_hot_water=None, provisions_small_multi_unit_heating=None, provisions_medium_multi_unit_heating=None, provisions_large_multi_unit_heating=None, provisions_small_multi_unit_hot_water=None, provisions_medium_multi_unit_hot_water=None, provisions_large_multi_unit_hot_water=None),
        ProductionSystem(identifier="electric_water_heater", is_heating=False, is_hot_water=True, is_individual=True, is_multi_unit=False, efficiency_heating=None, efficiency_hot_water=Decimal("1"), energy=energies["electricity"], is_hydro=False, enr_ratio_heating=None, enr_ratio_hot_water=Decimal("0"), investment_individual_heating=None, investment_individual_hot_water="500", investment_small_multi_unit_heating=None, investment_medium_multi_unit_heating=None, investment_large_multi_unit_heating=None, investment_small_multi_unit_hot_water=None, investment_medium_multi_unit_hot_water=None, investment_large_multi_unit_hot_water=None, maintenance_individual_heating=None, maintenance_individual_hot_water="0", maintenance_small_multi_unit_heating=None, maintenance_medium_multi_unit_heating=None, maintenance_large_multi_unit_heating=None, maintenance_small_multi_unit_hot_water=None, maintenance_medium_multi_unit_hot_water=None, maintenance_large_multi_unit_hot_water=None, provisions_small_multi_unit_heating=None, provisions_medium_multi_unit_heating=None, provisions_large_multi_unit_heating=None, provisions_small_multi_unit_hot_water=None, provisions_medium_multi_unit_hot_water=None, provisions_large_multi_unit_hot_water=None),
        ProductionSystem(identifier="ceti_outside_air", is_heating=False, is_hot_water=True, is_individual=True, is_multi_unit=False, efficiency_heating=None, efficiency_hot_water=Decimal("1.7"), energy=energies["electricity"], is_hydro=False, enr_ratio_heating=None, enr_ratio_hot_water=Decimal("0"), investment_individual_heating=None, investment_individual_hot_water="3000", investment_small_multi_unit_heating=None, investment_medium_multi_unit_heating=None, investment_large_multi_unit_heating=None, investment_small_multi_unit_hot_water=None, investment_medium_multi_unit_hot_water=None, investment_large_multi_unit_hot_water=None, maintenance_individual_heating=None, maintenance_individual_hot_water="100", maintenance_small_multi_unit_heating=None, maintenance_medium_multi_unit_heating=None, maintenance_large_multi_unit_heating=None, maintenance_small_multi_unit_hot_water=None, maintenance_medium_multi_unit_hot_water=None, maintenance_large_multi_unit_hot_water=None, provisions_small_multi_unit_heating=None, provisions_medium_multi_unit_heating=None, provisions_large_multi_unit_heating=None, provisions_small_multi_unit_hot_water=None, provisions_medium_multi_unit_hot_water=None, provisions_large_multi_unit_hot_water=None),
        ProductionSystem(identifier="ceti_inside_air", is_heating=False, is_hot_water=True, is_individual=True, is_multi_unit=False, efficiency_heating=None, efficiency_hot_water=Decimal("1.9"), energy=energies["electricity"], is_hydro=False, enr_ratio_heating=None, enr_ratio_hot_water=Decimal("0"), investment_individual_heating=None, investment_individual_hot_water="3000", investment_small_multi_unit_heating=None, investment_medium_multi_unit_heating=None, investment_large_multi_unit_heating=None, investment_small_multi_unit_hot_water=None, investment_medium_multi_unit_hot_water=None, investment_large_multi_unit_hot_water=None, maintenance_individual_heating=None, maintenance_individual_hot_water="100", maintenance_small_multi_unit_heating=None, maintenance_medium_multi_unit_heating=None, maintenance_large_multi_unit_heating=None, maintenance_small_multi_unit_hot_water=None, maintenance_medium_multi_unit_hot_water=None, maintenance_large_multi_unit_hot_water=None, provisions_small_multi_unit_heating=None, provisions_medium_multi_unit_heating=None, provisions_large_multi_unit_heating=None, provisions_small_multi_unit_hot_water=None, provisions_medium_multi_unit_hot_water=None, provisions_large_multi_unit_hot_water=None),
        ProductionSystem(identifier="ceti_extracted_air", is_heating=False, is_hot_water=True, is_individual=True, is_multi_unit=False, efficiency_heating=None, efficiency_hot_water=Decimal("2.3"), energy=energies["electricity"], is_hydro=False, enr_ratio_heating=None, enr_ratio_hot_water=Decimal("0"), investment_individual_heating=None, investment_individual_hot_water="4500", investment_small_multi_unit_heating=None, investment_medium_multi_unit_heating=None, investment_large_multi_unit_heating=None, investment_small_multi_unit_hot_water=None, investment_medium_multi_unit_hot_water=None, investment_large_multi_unit_hot_water=None, maintenance_individual_heating=None, maintenance_individual_hot_water="100", maintenance_small_multi_unit_heating=None, maintenance_medium_multi_unit_heating=None, maintenance_large_multi_unit_heating=None, maintenance_small_multi_unit_hot_water=None, maintenance_medium_multi_unit_hot_water=None, maintenance_large_multi_unit_hot_water=None, provisions_small_multi_unit_heating=None, provisions_medium_multi_unit_heating=None, provisions_large_multi_unit_heating=None, provisions_small_multi_unit_hot_water=None, provisions_medium_multi_unit_hot_water=None, provisions_large_multi_unit_hot_water=None),
        ProductionSystem(identifier="heat_pump_using_waste_heat", is_heating=True, is_hot_water=True, is_individual=False, is_multi_unit=True, efficiency_heating=Decimal("5.2"), efficiency_hot_water=Decimal("3.1"), energy=energies["electricity"], is_hydro=True, enr_ratio_heating=Decimal("0.503846153846154"), enr_ratio_hot_water=Decimal("0.167741935483871"), investment_individual_heating=None, investment_individual_hot_water=None, investment_small_multi_unit_heating="100000", investment_medium_multi_unit_heating="180000", investment_large_multi_unit_heating="300000", investment_small_multi_unit_hot_water="130000", investment_medium_multi_unit_hot_water="250000", investment_large_multi_unit_hot_water="400000", maintenance_individual_heating=None, maintenance_individual_hot_water=None, maintenance_small_multi_unit_heating="2000", maintenance_medium_multi_unit_heating="4000", maintenance_large_multi_unit_heating="8000", maintenance_small_multi_unit_hot_water="2500", maintenance_medium_multi_unit_hot_water="5000", maintenance_large_multi_unit_hot_water="10000", provisions_small_multi_unit_heating="3000", provisions_medium_multi_unit_heating="5400", provisions_large_multi_unit_heating="9000", provisions_small_multi_unit_hot_water="3900", provisions_medium_multi_unit_hot_water="7500", provisions_large_multi_unit_hot_water="12000"),
        ProductionSystem(identifier="heating_network", is_heating=True, is_hot_water=True, is_individual=False, is_multi_unit=True, efficiency_heating=Decimal("1"), efficiency_hot_water=Decimal("1"), energy=energies["network"], is_hydro=True, enr_ratio_heating=Decimal("0.6"), enr_ratio_hot_water=Decimal("0.6"), investment_individual_heating=None, investment_individual_hot_water=None, investment_small_multi_unit_heating="2000", investment_medium_multi_unit_heating="4000", investment_large_multi_unit_heating="6000", investment_small_multi_unit_hot_water="2000", investment_medium_multi_unit_hot_water="4000", investment_large_multi_unit_hot_water="6000", maintenance_individual_heating=None, maintenance_individual_hot_water=None, maintenance_small_multi_unit_heating="4300", maintenance_medium_multi_unit_heating="8600", maintenance_large_multi_unit_heating="12900", maintenance_small_multi_unit_hot_water="1000", maintenance_medium_multi_unit_hot_water="1500", maintenance_large_multi_unit_hot_water="2000", provisions_small_multi_unit_heating="4300", provisions_medium_multi_unit_heating="8600", provisions_large_multi_unit_heating="12900", provisions_small_multi_unit_hot_water="1000", provisions_medium_multi_unit_hot_water="1500", provisions_large_multi_unit_hot_water="2000"),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('energies', '0010_productionsystem'),
    ]

    operations = [
        migrations.RunPython(load_data, reverse_code=migrations.RunPython.noop),
    ]