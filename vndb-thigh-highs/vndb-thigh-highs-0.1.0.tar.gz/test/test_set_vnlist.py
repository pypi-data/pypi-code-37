from vndb_thigh_highs.models import VNList, PlayingStatus, User
from vndb_thigh_highs.models.operators import and_
from vndb_thigh_highs.error import TableUsedError
from test_case import LoggedInTestCase

class SetVNListTest(LoggedInTestCase):
    def test_set_vn(self):
        vn_id = 1297
        new_status = PlayingStatus.PLAYING
        new_notes = "Pretty great so far."
        filters = and_(VNList.user_id == 0, VNList.vn_id == vn_id)
        self.vndb.set_vnlist(vn_id, {
            VNList.status: new_status,
            VNList.notes: new_notes,
        })
        vnlists = self.vndb.get_vnlist(filters)
        self.assertEqual(len(vnlists), 1)
        vnlist = vnlists[0]
        self.assertEqual(vnlist.status, new_status)
        self.assertEqual(vnlist.notes, new_notes)
        self.vndb.delete_vnlist(vn_id)
        vnlists = self.vndb.get_vnlist(filters)
        self.assertEqual(len(vnlists), 0)

    def test_set_error(self):
        vn_id = 1297
        new_notes = 1
        try:
            self.vndb.set_vnlist(vn_id, {
                User.id: new_notes,
            })
            self.assertTrue(False)
        except TableUsedError as e:
            pass
