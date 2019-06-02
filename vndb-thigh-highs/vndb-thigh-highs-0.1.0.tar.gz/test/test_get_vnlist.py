from vndb_thigh_highs.models import Flag, VNList, PlayingStatus
from vndb_thigh_highs.models.operators import and_
from test_case import VNDBTestCase

class GetVnlistTest(VNDBTestCase):
    def test_vnlist(self):
        vnlists = self.vndb.get_vnlist(
            and_(VNList.user_id == 2, VNList.vn_id == 17),
            Flag.BASIC
        )
        self.assertEqual(len(vnlists), 1)
        vnlist = vnlists[0]
        self.assertEqual(vnlist.status, PlayingStatus.FINISHED)
