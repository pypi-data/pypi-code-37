import os
import unittest
from vndb_thigh_highs.dumps import VoteBuilder
from context import abspath
from test_case import TestCase

VOTES_PATH = abspath('../data/votes.txt')

@unittest.skipUnless(os.path.isfile(VOTES_PATH), "Missing data")
class VoteTest(TestCase):
    def test_votes(self):
        builder = VoteBuilder()
        votes = builder.build_with_file_path(VOTES_PATH)
