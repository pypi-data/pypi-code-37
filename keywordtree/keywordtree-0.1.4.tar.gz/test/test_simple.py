import unittest

from keywordtree import KeywordTree


class TestSimpleKeywordTree(unittest.TestCase):
    def setUp(self):
        dog_node = (['dog', 'woof'], [], '🐶')
        cat_node = (['cat', 'meow'], [], '🐱')
        self.kt = KeywordTree([], [dog_node, cat_node], None)

    def test_query(self):
        self.assertCountEqual(self.kt.query('Cat goes meow'), ['🐱'])
