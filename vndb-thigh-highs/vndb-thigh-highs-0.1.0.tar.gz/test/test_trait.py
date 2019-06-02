import os
import unittest
from vndb_thigh_highs.dumps import TraitDatabaseBuilder
from context import abspath
from test_case import TestCase

TRAITS_PATH = abspath('../data/traits.json')

@unittest.skipUnless(os.path.isfile(TRAITS_PATH), "Missing data")
class TraitTest(TestCase):
    def test_red_eye(self):
        builder = TraitDatabaseBuilder()
        trait_database = builder.build_with_file_path(TRAITS_PATH)
        trait = trait_database.get_trait(115)
        self.assertEqual(trait.name, "Red")
        self.assertFalse(trait.meta)
        self.assertEqual(len(trait.parents), 1)
        self.assertEqual(len(trait.children), 0)
        for parent_trait in trait.parents:
            self.assertEqual(parent_trait.name, "Eye Color")
            self.assertTrue(parent_trait.meta)
