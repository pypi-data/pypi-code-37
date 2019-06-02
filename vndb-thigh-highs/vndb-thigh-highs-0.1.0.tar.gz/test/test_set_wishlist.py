from vndb_thigh_highs.models import Wishlist, Priority
from vndb_thigh_highs.models.operators import and_
from test_case import LoggedInTestCase

class SetWishlistTest(LoggedInTestCase):
    def test_set_vn(self):
        vn_id = 11725
        new_priority = Priority.HIGH
        filters = and_(Wishlist.user_id == 0, Wishlist.vn_id == vn_id)
        self.vndb.set_wishlist(vn_id, {
            Wishlist.priority: new_priority,
        })
        wishlists = self.vndb.get_wishlist(filters)
        self.assertEqual(len(wishlists), 1)
        wishlist = wishlists[0]
        self.assertEqual(Wishlist.priority, new_priority)
        self.vndb.delete_wishlist(vn_id)
        wishlists = self.vndb.get_wishlist(filters)
        self.assertEqual(len(wishlists), 0)
