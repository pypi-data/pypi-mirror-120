import shutil
import tempfile

import numpy as np

import resdk
from resdk.tables import RNATables

from ..base import BaseResdkFunctionalTest


class TestTables(BaseResdkFunctionalTest):
    @classmethod
    def setUpClass(cls):
        cls.cache_dir = tempfile.mkdtemp()
        cls.test_server_url = "https://app.genialis.com"
        cls.test_collection_slug = "resdk-test-collection-tables"
        cls.res = resdk.Resolwe(
            url=cls.test_server_url, username="resdk-e2e-test", password="safe4ever"
        )
        cls.collection = cls.res.collection.get(cls.test_collection_slug)
        cls.ct = RNATables(cls.collection, cache_dir=cls.cache_dir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.cache_dir)

    def test_meta(self):
        self.assertEqual(self.ct.meta.shape, (8, 9))
        self.assertIn("Copy of SUM149_JQ1_12H_R1", self.ct.meta.index)
        self.assertIn("general.species", self.ct.meta.columns)

    def test_rc(self):
        self.assertEqual(self.ct.rc.shape, (8, 58487))
        self.assertIn("Copy of SUM149_JQ1_12H_R1", self.ct.rc.index)
        self.assertIn("ENSG00000000003", self.ct.rc.columns)
        self.assertEqual(self.ct.rc.iloc[0, 0], 1580)
        self.assertIsInstance(self.ct.rc.iloc[0, 0], np.int64)

    def test_exp(self):
        self.assertEqual(self.ct.exp.shape, (8, 58487))
        self.assertIn("Copy of SUM149_JQ1_12H_R1", self.ct.exp.index)
        self.assertIn("ENSG00000000003", self.ct.exp.columns)
        self.assertAlmostEqual(self.ct.exp.iloc[0, 0], 32.924003, places=3)
        self.assertIsInstance(self.ct.exp.iloc[0, 0], np.float64)

    def test_consistent_index(self):
        self.assertTrue(all(self.ct.exp.index == self.ct.meta.index))
        self.assertTrue(all(self.ct.rc.index == self.ct.meta.index))
