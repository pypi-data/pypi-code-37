from vndb_thigh_highs.models import Flag, Votelist
from vndb_thigh_highs.models.operators import and_
from test_case import VNDBTestCase

class GetVotelistTest(VNDBTestCase):
    def test_votelist(self):
        votelists = self.vndb.get_votelist(
            and_(Votelist.user_id == 2, Votelist.vn_id == 17),
            Flag.BASIC
        )
        self.assertEqual(len(votelists), 1)
        votelist = votelists[0]
        self.assertEqual(votelist.vote, 100)
