import copy
import json
from decimal import Decimal

from django.test import TestCase
from energies.models import Energy, ProductionSystem
from thermix.libs import Compute


class ComputeTestCase(TestCase):
    def setUp(self):
        self.ensure_energies_values([3, 5])

        with open("./thermix/tests/individual_simulation.json") as json_file:
            self.data = json.load(json_file)

        self.compute = Compute(self.data)
        self.systems_results = []
        for system_type in ["heating", "hot_water"]:
            for system_data in self.data["solutions"][0][system_type + "_systems"]:
                if not system_data["production_system"] == 0:
                    system = ProductionSystem.objects.get(
                        pk=system_data["production_system"]
                    )
                    self.__ensure_system_values(system)
                    computed_system_data = self.compute.compute_system(
                        system_type, system_data
                    )
                    self.systems_results.append({**system_data, **computed_system_data})

    def ensure_energies_values(self, energies_pk):
        for energy_pk in energies_pk:
            energy = Energy.objects.get(pk=energy_pk)
            if energy_pk == 3:
                energy.combustible_category = "fossil"
                energy.ghg_ratio = Decimal("0.234")
                energy.primary_energy_ratio = Decimal("1")
            if energy_pk == 5:
                energy.combustible_category = "electricity"
                energy.ghg_ratio = Decimal("0.18")
                energy.primary_energy_ratio = Decimal("2.58")
            if energy_pk == 8:
                energy.combustible_category = "renewable"
                energy.ghg_ratio = Decimal("0.013")
                energy.primary_energy_ratio = Decimal("0.6")
            energy.save()

    def __ensure_system_values(self, system):
        if system.pk == 4:
            system.enr_ratio_heating = Decimal("0")
            system.enr_ratio_hot_water = Decimal("0")
        if system.pk == 9:
            system.enr_ratio_heating = Decimal("1")
            system.enr_ratio_hot_water = Decimal("1")
        if system.pk == 13:
            system.enr_ratio_heating = Decimal("0.503846153846154")
            system.enr_ratio_hot_water = Decimal("0.17")
        system.save()

    def test_compute_system(self):
        ref_results = {
            "identifier": "thermodynamic_cmv",
            "label": "VMC thermodynamique",
            "type": "heating",
            "carbon_emission": Decimal("407.2398190045248955725785081"),
            "combustible_cost_by_year": Decimal("479.7176757602273100491388271"),
            "combustible_costs": [
                Decimal("356.3348416289592836260061946"),
                Decimal("367.0961538461538544009691173"),
                Decimal("378.1824576923077012257015377"),
                Decimal("389.6035679146153942372799364"),
                Decimal("401.3695956656367795909317817"),
                Decimal("413.4909574547390107957840296"),
                Decimal("425.9783843698721293969512402"),
                Decimal("438.8429315778422681942227631"),
                Decimal("452.0959881114931051979542906"),
                Decimal("465.7492869524601974944273435"),
                Decimal("479.8149154184244959939426262"),
                Decimal("494.3053258640609163243058150"),
                Decimal("509.2333467051555565652966245"),
                Decimal("524.6121937756512549587188594"),
                Decimal("540.4554820276759234612939840"),
                Decimal("556.7772375849117369708520960"),
                Decimal("573.5919101599760720671538798"),
                Decimal("590.9143858468073501026853952"),
                Decimal("608.7600002993809327547948869"),
                Decimal("627.1445523084222376235041391"),
            ],
            "final_energy_consumption": Decimal("2262.443438914027197625436156"),
            "final_energy_consumption_by_year": Decimal(
                "113.1221719457013598812718078"
            ),
            "primary_energy_consumption": Decimal("5837.104072398190169873625282"),
            "renewable_heating_production": Decimal("5882.352941176470914771477830"),
            "system_output_heating_production": Decimal(
                "11764.70588235294182954295566"
            ),
            "taxable_carbon_emission": 0,
            "useful_heating_production": Decimal("10000.00000000000055511151231"),
            # "useful_heating_production_by_year": Decimal(
            #     "500.0000000000000277555756155"
            # ),
            "secondary_efficiency": Decimal("0.8500000000"),
        }

        system_data = self.data["solutions"][0]["heating_systems"][1]

        computed_results = self.compute.compute_system("heating", system_data)

        self.maxDiff = None
        self.assertDictEqual(ref_results, computed_results)

    def test_compute_period_total_cost(self):
        ref_results = {
            # "carbon_tax": Decimal("25345.25721362229361341152221"),
            "combustible_cost": Decimal("167250.6965756690208399805980"),
            "financial_support_amount": None,
            "investment": 15000,
            "maintenance_cost": 12000,
            "overall_total": Decimal("194250.6965756690208399805980"),
            "overall_total_by_year": Decimal("9712.5348287834510419990299"),
            "provisions_cost": 0,
        }

        computed_results = self.compute.compute_period_total_cost(
            self.data["solutions"][0], self.systems_results
        )

        self.maxDiff = None
        self.assertDictEqual(ref_results, computed_results)

    def test_compute_period_cost_evolution(self):
        ref_results = [
            {"cumulated_cost": Decimal("21390.83223001766892328097017"), "year": 2019},
            {"cumulated_cost": Decimal("27996.08878282155133793498726"), "year": 2020},
            {"cumulated_cost": Decimal("34823.72742688655506367996938"), "year": 2021},
            {"cumulated_cost": Decimal("41882.00181435079154346350231"), "year": 2022},
            {"cumulated_cost": Decimal("49179.47249943914722267858541"), "year": 2023},
            {"cumulated_cost": Decimal("56725.01836772185680026094811"), "year": 2024},
            {"cumulated_cost": Decimal("64527.84849154246489552612532"), "year": 2025},
            {"cumulated_cost": Decimal("72597.51442752240542132100039"), "year": 2026},
            {"cumulated_cost": Decimal("80943.92297264368521329413033"), "year": 2027},
            {"cumulated_cost": Decimal("89577.34939602763123335267647"), "year": 2028},
            {"cumulated_cost": Decimal("98508.45116416717991415704104"), "year": 2029},
            {"cumulated_cost": Decimal("107748.2821780336150094228940"), "year": 2030},
            {"cumulated_cost": Decimal("117308.3075411668909917877993"), "year": 2031},
            {"cumulated_cost": Decimal("127200.4188785726403950942231"), "year": 2032},
            {"cumulated_cost": Decimal("137436.9502269896180523024117"), "year": 2033},
            {"cumulated_cost": Decimal("148030.6945178596814771004620"), "year": 2034},
            {"cumulated_cost": Decimal("158994.9206751294805905410201"), "year": 2035},
            {"cumulated_cost": Decimal("170343.3913508399062874448871"), "year": 2036},
            {"cumulated_cost": Decimal("182090.3813223171408759683364"), "year": 2037},
            {"cumulated_cost": Decimal("194250.6965756690208399805979"), "year": 2038},
        ]

        computed_results = self.compute.compute_period_cost_evolution(
            self.data["solutions"][0], self.systems_results
        )

        self.maxDiff = None
        self.assertListEqual(ref_results, computed_results)

    def test_compute_environmental_indicators(self):
        ref_results = {
            "carbon_report": Decimal("12956.42549448463951679162985"),
            # "carbon_report_by_year": Decimal("647.8212747242319758395814925"),
            "carbon_report_km_equivalent": Decimal("2811.544332303166775143783677"),
            # "carbon_report_km_equivalent_by_year": Decimal(
            #     "140.5772166151583387571891838"
            # ),
            "final_energy_consumption": Decimal("83726.52735842658539015925516"),
            # "final_energy_consumption_by_year": Decimal(
            #     "4186.326367921329269507962758"
            # ),
            "primary_energy_consumption": Decimal("74529.79591017383856665477309"),
            # "primary_energy_consumption_by_year": Decimal(
            #     "3726.489795508691928332738654"
            # ),
            "renewable_electricity": 9000,
            "renewable_heating_production": Decimal("28870.85868830290769638067323"),
            "renewable_heating_production_network_only": 0,
            "renewable_heating_production_ratio": Decimal(
                "0.3528925619834710642864704045"
            ),
            "renewable_production_ratio": Decimal("0.4170246666319214246706437554"),
            "renewable_heating_production_without_network": Decimal(
                "28870.85868830290769638067323"
            ),
            "total_renewable_production": Decimal("37870.85868830290769638067323"),
            "total_renewable_production_without_network": Decimal(
                "37870.85868830290769638067323"
            ),
        }

        computed_results = self.compute.compute_environmental_indicators(
            self.data["solutions"][0], self.systems_results
        )

        self.maxDiff = None
        self.assertDictEqual(ref_results, computed_results)

    def test_compute_solution(self):
        computed_solution = self.compute.compute_solution(self.data["solutions"][0])

        keys = [
            "systems_results",
            "period_total_cost",
            "period_cost_evolution",
            "environmental_indicators",
        ]
        self.assertTrue(all(key in computed_solution for key in keys))

    def test_compute_solutions(self):
        computed_solutions = self.compute.compute_solutions()

        self.assertEqual(len(computed_solutions), 4)

        keys = [
            "index",
            "systems_labels",
            "period_total_cost",
            "period_cost_evolution",
            "environmental_indicators",
        ]
        self.assertTrue(all(key in computed_solutions[0] for key in keys))

    def test_financial_support(self):
        computed_solution = self.compute.compute_solution(self.data["solutions"][3])
        #  5000 = 8000(sum of investments) - 3000 (financial support)
        self.assertEqual(5000, computed_solution["period_total_cost"]["investment"])

        solution_no_fin_supp = copy.copy(self.data["solutions"][3])
        solution_no_fin_supp["financial_support"] = False
        computed_solution_no_fin_supp = self.compute.compute_solution(
            solution_no_fin_supp
        )
        first_year_cumulated_cost_no_fin_supp = computed_solution_no_fin_supp[
            "period_cost_evolution"
        ][0]["cumulated_cost"]

        self.assertEqual(
            first_year_cumulated_cost_no_fin_supp - 3000,
            computed_solution["period_cost_evolution"][0]["cumulated_cost"],
        )


class ComputeThermalSolarTestCase(ComputeTestCase):
    def setUp(self):
        self.ensure_energies_values([3, 5])

        with open(
            "./thermix/tests/individual_thermal_solar_simulation.json"
        ) as json_file:
            self.data = json.load(json_file)

        self.compute = Compute(self.data)
        self.systems_results = self.compute.compute_systems_thermal_solar(
            self.data["solutions"][0]
        )

    def test_compute_system(self):
        pass

    def test_compute_environmental_indicators(self):
        pass

    def test_compute_period_cost_evolution(self):
        pass

    def test_financial_support(self):
        pass

    def test_compute_thermal_solar_system(self):
        ref_results = {
            "carbon_emission": Decimal("0"),
            "combustible_cost_by_year": Decimal("0"),
            "combustible_costs": [
                Decimal("0"),
                Decimal("0"),
                Decimal("0"),
                Decimal("0"),
                Decimal("0"),
                Decimal("0"),
                Decimal("0"),
                Decimal("0"),
                Decimal("0"),
                Decimal("0"),
                Decimal("0"),
                Decimal("0"),
                Decimal("0"),
                Decimal("0"),
                Decimal("0"),
                Decimal("0"),
                Decimal("0"),
                Decimal("0"),
                Decimal("0"),
                Decimal("0"),
            ],
            "final_energy_consumption": Decimal("0"),
            "final_energy_consumption_by_year": Decimal("0"),
            "primary_energy_consumption": Decimal("0"),
            "renewable_heating_production": Decimal("2250"),
            "system_output_heating_production": Decimal("0"),
            "taxable_carbon_emission": 0,
            "useful_heating_production": Decimal("2250.00"),
            # "useful_heating_production_by_year": Decimal("112.5"),
            "solar_production": Decimal("2250.00"),
            "secondary_efficiency": Decimal("0"),
            "identifier": "solar_system_combined",
            "label": "Système Solaire Combiné",
            "type": "heating",
            "estimated_investment": 10000,
            "maintenance_cost": 500,
            "provisions_cost": 0,
        }

        heating_solar_system_data = self.data["solutions"][0]["heating_systems"][1]

        computed_results = self.compute.compute_thermal_solar_system(
            "heating", heating_solar_system_data
        )

        self.maxDiff = None
        self.assertDictEqual(ref_results, computed_results)

        computed_results_with_already_solar_consumed = self.compute.compute_thermal_solar_system(
            "heating", heating_solar_system_data, Decimal("3000")
        )

        self.maxDiff = None
        self.assertEqual(
            Decimal("1500"),
            computed_results_with_already_solar_consumed["solar_production"],
        )

    def test_compute_period_total_cost(self):
        ref_results = {
            # "carbon_tax": Decimal("6177.906445820434147409681396"),
            "combustible_cost": Decimal("27364.62989407049733035543353"),
            "financial_support_amount": None,
            "investment": 20000,
            "maintenance_cost": 28000,
            "overall_total": Decimal("75364.62989407049733035543353"),
            "overall_total_by_year": Decimal("3768.231494703524866517771676"),
            "provisions_cost": 0,
        }

        computed_results = self.compute.compute_period_total_cost(
            self.data["solutions"][0], self.systems_results
        )

        self.maxDiff = None
        self.assertDictEqual(ref_results, computed_results)

    def test_is_solution_contain_thermal_solar(self):
        self.assertEqual(
            True,
            self.compute.is_solution_contain_thermal_solar(self.data["solutions"][0]),
        )

        self.assertEqual(
            False,
            self.compute.is_solution_contain_thermal_solar(self.data["solutions"][1]),
        )

    def test_ordered_systems_with_thermal_solar_first(self):
        systems_data = self.data["solutions"][0]["heating_systems"]
        ordered_systems = self.compute.ordered_systems_with_thermal_solar_first(
            systems_data
        )
        self.assertEqual(27, ordered_systems[0]["production_system"])
        self.assertEqual(4, ordered_systems[1]["production_system"])
        self.assertEqual(True, ordered_systems[0]["is_thermal_solar"])
        self.assertEqual(False, "is_thermal_solar" in ordered_systems[1].keys())
