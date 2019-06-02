import os
import unittest
from vndb_thigh_highs.dumps import TagDatabaseBuilder
from context import abspath
from test_case import TestCase

TAGS_PATH = abspath('../data/tags.json')

@unittest.skipUnless(os.path.isfile(TAGS_PATH), "Missing data")
class TagTest(TestCase):
    def test_only_a_single_heroine(self):
        builder = TagDatabaseBuilder()
        tag_database = builder.build_with_file_path(TAGS_PATH)
        tag = tag_database.get_tag(268)
        self.assertEqual(tag.name, "Only a Single Heroine")
        self.assertFalse(tag.meta)
        self.assertEqual(len(tag.parents), 1)
        self.assertEqual(len(tag.children), 0)
        for parent_tag in tag.parents:
            self.assertEqual(parent_tag.name, "Heroine")
            self.assertTrue(parent_tag.meta)
