from vndb_thigh_highs.models import Flag, VN, User
from vndb_thigh_highs.error import TableUsedError
from vndb_thigh_highs import GetCommandOptions
from test_case import VNDBTestCase

class GetVNTest(VNDBTestCase):
    def test_vn_basic(self):
        vns = self.vndb.get_vn(VN.id == 17, Flag.BASIC)
        self.assertEqual(len(vns), 1)
        vn = vns[0]
        self.assertEqual(vn.title, "Ever17 -The Out of Infinity-")
        self.assertEqual(vn.id, 17)

    def test_vn_all_flags(self):
        vns = self.vndb.get_vn(VN.id == 17)
        self.assertEqual(len(vns), 1)
        vn = vns[0]
        self.assertEqual(vn.image_nsfw, False)
        self.assertGreater(vn.popularity, 40)

    def test_vn_aliases(self):
        vns = self.vndb.get_vn(VN.id == 5154, Flag.DETAILS)
        self.assertEqual(len(vns), 1)
        vn = vns[0]
        self.assertIsInstance(vn.aliases, list)
        self.assertIn("Grikaji", vn.aliases)

    def test_vn_sort(self):
        options = GetCommandOptions()
        options.sort = VN.popularity
        options.reverse = True
        vns = self.vndb.get_vn(VN.id == [4, 17968], Flag.BASIC, options)
        self.assertEqual(vns[0].id, 4)
        self.assertEqual(vns[1].id, 17968)

    def test_sort_error(self):
        options = GetCommandOptions()
        options.sort = User.id
        try:
            self.vndb.get_vn(VN.id == 1, Flag.BASIC, options)
            self.assertTrue(False)
        except TableUsedError as e:
            pass

    def test_filter_error(self):
        try:
            self.vndb.get_vn(User.id == 1)
            self.assertTrue(False)
        except TableUsedError as e:
            pass
