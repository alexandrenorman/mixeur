# -*- coding: utf-8 -*-

import datetime

from test_plus.test import TestCase

from custom_exports.helpers import DataAdapter


class DataAdapterTestCase(TestCase):
    def test_convert_date(self):
        date = datetime.datetime.now()
        self.assertEqual(
            DataAdapter._convert_date(value=date, arg="%Y-%m-%d"),
            date.strftime("%Y-%m-%d"),
        )

    def test_convert_nop(self):
        self.assertEqual(
            DataAdapter._convert_nop(value="AUIRESTAUIRT", arg="fixed"),
            "AUIRESTAUIRT",
        )

        self.assertEqual(
            DataAdapter._convert_nop(value=12.3, arg="fixed"),
            12.3,
        )

    def test_convert_fixed(self):
        self.assertEqual(
            DataAdapter._convert_fixed(value="AUIRESTAUIRT", arg="fixed"),
            "fixed",
        )

    def test_convert_html(self):
        self.assertEqual(
            DataAdapter._convert_html(
                value="<p>Test de mise en page.<br><b>retour</b> à la ligne.</p>",
                arg=None,
            ),
            "Test de mise en page.    **retour** à la ligne.",
        )

    def test_convert_int(self):
        self.assertEqual(
            DataAdapter._convert_int(value="12", arg="any"),
            12,
        )
        self.assertEqual(
            DataAdapter._convert_int(value="012", arg="any"),
            12,
        )
        self.assertEqual(
            DataAdapter._convert_int(value="-12", arg="any"),
            -12,
        )
        with self.assertRaises(DataAdapter.DataAdapterError):
            self.assertEqual(
                DataAdapter._convert_int(value="12.1", arg="any"),
                12,
            )
        with self.assertRaises(DataAdapter.DataAdapterError):
            DataAdapter._convert_int(value="BÉPO", arg="any")

        self.assertEqual(
            DataAdapter._convert_int(value="BÉPO", arg="any", default="50"),
            50,
        )

    def test_convert_float(self):
        self.assertEqual(
            DataAdapter._convert_float(value="12", arg="any"),
            12,
        )
        self.assertEqual(
            DataAdapter._convert_float(value="-12", arg="any"),
            -12,
        )
        self.assertEqual(
            DataAdapter._convert_float(value="12.1", arg="any"),
            12.1,
        )
        self.assertEqual(
            DataAdapter._convert_float(value="012.1", arg="any"),
            12.1,
        )
        with self.assertRaises(DataAdapter.DataAdapterError):
            DataAdapter._convert_float(value="BÉPO", arg="any")

    def test_convert_bool(self):
        booldata = {
            True: "Oui",
            False: "Non",
        }
        self.assertEqual(DataAdapter._convert_bool(value=True, arg=booldata), "Oui")
        self.assertEqual(DataAdapter._convert_bool(value=False, arg=booldata), "Non")
        with self.assertRaises(DataAdapter.DataAdapterError):
            DataAdapter._convert_list(value=None, arg=booldata)
            DataAdapter._convert_list(value=12, arg=booldata)
            DataAdapter._convert_list(value="bépo", arg=booldata)

    def test_convert_list(self):
        listdata = {
            "First choice": "choice_1",
            "Second choice": "choice_2",
        }
        self.assertEqual(DataAdapter._convert_list(value="", arg=listdata), "")
        self.assertEqual(DataAdapter._convert_list(value=None, arg=listdata), "")
        self.assertEqual(
            DataAdapter._convert_list(value="First choice", arg=listdata), "choice_1"
        )
        self.assertEqual(
            DataAdapter._convert_list(value="Second choice", arg=listdata), "choice_2"
        )
        with self.assertRaises(DataAdapter.DataAdapterError):
            DataAdapter._convert_list(value="Non existing choice", arg=listdata)

    def test_convert_list_with_default(self):
        listdata = {
            "First choice": "choice_1",
            "Second choice": "choice_2",
        }
        self.assertEqual(
            DataAdapter._convert_list(value="", arg=listdata, default="choice_3"), ""
        )
        self.assertEqual(
            DataAdapter._convert_list(value=None, arg=listdata, default="choice_3"), ""
        )
        self.assertEqual(
            DataAdapter._convert_list(
                value="First choice", arg=listdata, default="choice_3"
            ),
            "choice_1",
        )
        self.assertEqual(
            DataAdapter._convert_list(
                value="Second choice", arg=listdata, default="choice_3"
            ),
            "choice_2",
        )
        self.assertEqual(
            DataAdapter._convert_list(
                value="Another choice", arg=listdata, default="choice_3"
            ),
            "choice_3",
        )

    def test_convert_list_multiple(self):
        listdata = {
            "First choice": "choice_1",
            "Second choice": "choice_2",
            "Third choice": "choice_3",
        }
        self.assertEqual(
            DataAdapter._convert_list_multiple(value=["First choice"], arg=listdata),
            "choice_1",
        )
        self.assertEqual(
            DataAdapter._convert_list_multiple(
                value=["First choice", "Second choice"], arg=listdata
            ),
            "choice_1, choice_2",
        )
        self.assertEqual(
            DataAdapter._convert_list_multiple(value=None, arg=listdata), ""
        )
        self.assertEqual(DataAdapter._convert_list_multiple(value="", arg=listdata), "")
        self.assertEqual(DataAdapter._convert_list_multiple(value=[], arg=listdata), "")
        with self.assertRaises(DataAdapter.DataAdapterError):
            self.assertEqual(
                DataAdapter._convert_list_multiple(
                    value=["Non existing choice"], arg=listdata
                ),
                "",
            )

    def test_convert_list_multiple_with_default(self):
        listdata = {
            "First choice": "choice_1",
            "Second choice": "choice_2",
            "Third choice": "choice_3",
        }
        self.assertEqual(
            DataAdapter._convert_list_multiple(
                value=["First choice"], arg=listdata, default="choice_4"
            ),
            "choice_1",
        )
        self.assertEqual(
            DataAdapter._convert_list_multiple(
                value=["First choice", "Second choice"],
                arg=listdata,
                default="choice_4",
            ),
            "choice_1, choice_2",
        )
        self.assertEqual(
            DataAdapter._convert_list_multiple(
                value=None, arg=listdata, default="choice_4"
            ),
            "",
        )
        self.assertEqual(
            DataAdapter._convert_list_multiple(
                value="", arg=listdata, default="choice_4"
            ),
            "",
        )
        self.assertEqual(
            DataAdapter._convert_list_multiple(
                value=[], arg=listdata, default="choice_4"
            ),
            "",
        )

        self.assertEqual(
            DataAdapter._convert_list_multiple(
                value=["Non existing choice"], arg=listdata, default="choice_4"
            ),
            "choice_4",
        )
        self.assertEqual(
            DataAdapter._convert_list_multiple(
                value=[
                    "First choice",
                    "Non existing choice",
                    "Another non existing choice",
                ],
                arg=listdata,
                default="choice_4",
            ),
            "choice_4, choice_1",
        )
