# -*- coding: utf-8 -*-

import json

# import os
import shutil
import tempfile
from pathlib import Path

from mock.mock import PropertyMock, patch
from test_plus.test import TestCase

from white_labelling.helpers import wl_cdn

from .factories import WhiteLabellingFactory


class WlCdnHelperCase(TestCase):
    def setUp(self, *args):
        self.tmp_dir = tempfile.mkdtemp()
        # We define a defaule dir different to the normal one to not interfer with existing files
        patcher = patch(
            "white_labelling.models.WhiteLabelling.cdn_default_directory_path",
            new_callable=PropertyMock,
            return_value=self.tmp_dir,
        )
        patcher.start()

        with self.settings(SKIP_TRAEFIK_AUTOCONFIG_ON_WL_SAVE=True):
            self.wl = WhiteLabellingFactory()

        self.json_data = {
            "truc1": 1,
            "truc2": 2,
            "demo": {
                "text_a": "Tralala pouet pouet",
                "text_format": "L'armée des {monkeysCount} singes",
            },
            "machin": {"chose": {"chouette": 42}},
        }
        self.json_path = Path(self.wl.cdn_directory_path, "test1.json")
        with self.json_path.open("w") as f:
            f.write(json.dumps(self.json_data))

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
        shutil.rmtree(self.wl.cdn_directory_path)
        self.wl.delete()

    def test_read_data(self, *args):
        json_data = wl_cdn.read_data(self.wl).get("test1")
        self.assertDictEqual(self.json_data, json_data)

    def test_read_data_merge_with_default(self):
        default_json_data = {"truc1": 42, "truc_new": 42}
        default_json_path = Path(self.wl.cdn_default_directory_path, "test1.json")
        with default_json_path.open("w") as f:
            f.write(json.dumps(default_json_data))

        expected_json_data = {**default_json_data, **self.json_data}
        readed_json_data = wl_cdn.read_data(self.wl).get("test1")
        self.assertDictEqual(expected_json_data, readed_json_data)

        # default_json_path.unlink()

    def test_read_data_cache(self):
        # Initial read to ensure cache is feeded
        json_data = wl_cdn.read_data(self.wl).get("test1")
        # self.assertDictEqual(self.json_data, json_data)

        # Change json content in same file
        new_json_data = {"truc1": 800}
        with self.json_path.open("w") as f:
            f.write(json.dumps(new_json_data))

        # Check data is still the old ones (self.json_data)
        json_data = wl_cdn.read_data(self.wl).get("test1")
        self.assertDictEqual(self.json_data, json_data)

        # Re-check without using cache, data should be th new ones (new_json_data)
        json_data = wl_cdn.read_data(self.wl, no_cache=True).get("test1")
        self.assertDictEqual(new_json_data, json_data)

    def test_get_data(self):
        self.assertEqual(1, wl_cdn.get_data(self.wl, path="test1.truc1"))
        self.assertIsNone(wl_cdn.get_data(self.wl, path="test1.truc3"))
        self.assertDictEqual(
            {"chouette": 42}, wl_cdn.get_data(self.wl, path="test1.machin.chose")
        )

    def test_get_text(self):
        self.assertEqual(
            "Tralala pouet pouet", wl_cdn.get_text(self.wl, path="test1.demo.text_a")
        )
        self.assertEqual(
            "", wl_cdn.get_text(self.wl, path="test1.demo.text_not_exists")
        )
        self.assertEqual(
            "plouf",
            wl_cdn.get_text(
                self.wl, path="test1.demo.text_not_exists", fallback="plouf"
            ),
        )
        self.assertEqual(
            "L'armée des 12 singes",
            wl_cdn.get_text(
                self.wl, path="test1.demo.text_format", params={"monkeysCount": 12}
            ),
        )
        self.assertEqual(
            "L'armée des  singes",
            wl_cdn.get_text(self.wl, path="test1.demo.text_format"),
        )
        self.assertEqual(
            "Il y a 42 pots de fleurs",
            wl_cdn.get_text(
                self.wl,
                path="test1.demo.text_format_not_exists",
                params={"serviette": 42},
                fallback="Il y a {serviette} pots de fleurs",
            ),
        )
