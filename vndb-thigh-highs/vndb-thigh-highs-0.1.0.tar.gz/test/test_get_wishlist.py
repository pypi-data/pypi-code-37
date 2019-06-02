from vndb_thigh_highs.models import Flag, Wishlist, Priority
from vndb_thigh_highs.models.operators import and_
from test_case import VNDBTestCase

class GetWishlistTest(VNDBTestCase):
    def test_wishlist(self):
        wishlists = self.vndb.get_wishlist(
            and_(Wishlist.user_id == 2, Wishlist.vn_id == 1320),
            Flag.BASIC
        )
        self.assertEqual(len(wishlists), 1)
        wishlist = wishlists[0]
        self.assertEqual(wishlist.priority, Priority.LOW)
