import unittest
from vndb_thigh_highs.models import VN
from test_case import VNDBTestCase

class ThrottledTest(VNDBTestCase):
    @unittest.skip("This test is long. Do it once in a while.")
    def test_throttled(self):
        # No sure way to get a throttled error,
        # ask a lot of data from the server to try to have it.
        for i in range(0, 8):
            self.vndb.get_all_vn(VN.id == list(range(1, 50)))
