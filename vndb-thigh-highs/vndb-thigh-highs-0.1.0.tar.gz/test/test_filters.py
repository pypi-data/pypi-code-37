from vndb_thigh_highs.models import VN
from vndb_thigh_highs.models.operators import and_, or_, search
from test_case import TestCase

class FilterTest(TestCase):
    def test_eq(self):
        filters = VN.id == 1
        self.assertEqual(str(filters), "id = 1")

    def test_ne(self):
        filters = VN.id != 1
        self.assertEqual(str(filters), "id != 1")

    def test_le(self):
        filters = VN.released_date <= 2010
        self.assertEqual(str(filters), "released <= 2010")

    def test_lt(self):
        filters = VN.released_date < 2010
        self.assertEqual(str(filters), "released < 2010")

    def test_ge(self):
        filters = VN.released_date >= 2010
        self.assertEqual(str(filters), "released >= 2010")

    def test_gt(self):
        filters = VN.released_date > 2010
        self.assertEqual(str(filters), "released > 2010")


    def test_eq_array(self):
        filters = VN.id == [1, 2, 3]
        self.assertEqual(str(filters), "id = [1, 2, 3]")

    def test_ne_array(self):
        filters = VN.id != [2, 5, 1]
        self.assertEqual(str(filters), "id != [2, 5, 1]")


    def test_eq_str(self):        
        filters = VN.title == 'fsn'
        self.assertEqual(str(filters), "title = fsn")


    def test_and(self):
        filters = and_(VN.id == 1, VN.id != 8)
        self.assertEqual(str(filters), "id = 1 and id != 8")

    def test_or(self):
        filters = or_(VN.id == 1, VN.id != 8)
        self.assertEqual(str(filters), "id = 1 or id != 8")

    def test_search_title(self):
        filters = search(VN.title, 'ever17')
        self.assertEqual(str(filters), "title ~ ever17")


    def test_search(self):
        filters = search(VN.search, 'ever17')
        self.assertEqual(str(filters), "search ~ ever17")
