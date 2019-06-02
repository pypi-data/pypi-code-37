from test_case import VNDBTestCase

class DBStatsTest(VNDBTestCase):
    def test_dbstats(self):
        dbstats = self.vndb.dbstats()
        self.assertTrue(dbstats.releases > 50000)
        self.assertTrue(dbstats.characters > 70000)

