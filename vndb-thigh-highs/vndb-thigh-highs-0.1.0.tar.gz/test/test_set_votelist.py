from vndb_thigh_highs.models import Votelist
from vndb_thigh_highs.models.operators import and_
from vndb_thigh_highs.error import ResponseError, ResponseErrorId
from test_case import LoggedInTestCase

class SetVotelistTest(LoggedInTestCase):
    def test_set_vote(self):
        vn_id = 2153
        new_vote = 50
        filters = and_(Votelist.user_id == 0, Votelist.vn_id == vn_id)
        self.vndb.set_votelist(vn_id, {
            Votelist.vote: new_vote,
        })
        votelists = self.vndb.get_votelist(filters)
        self.assertEqual(len(votelists), 1)
        votelist = votelists[0]
        self.assertEqual(votelist.vote, new_vote)
        self.vndb.delete_votelist(vn_id)
        votelists = self.vndb.get_votelist(filters)
        self.assertEqual(len(votelists), 0)

    def test_set_type_error(self):
        try:
            self.vndb.set_votelist(2153, {Votelist.vn_id: 2})
            self.assertTrue(False)
        except ResponseError as e:
            self.assertEqual(e.id, ResponseErrorId.MISSING)
