from vndb_thigh_highs.models import Flag, User
from test_case import VNDBTestCase

class GetUserTest(VNDBTestCase):
    def test_user(self):
        users = self.vndb.get_user(User.id == 2, Flag.BASIC)
        self.assertEqual(len(users), 1)
        user = users[0]
        self.assertEqual(user.username, "yorhel")
        self.assertEqual(user.id, 2)
