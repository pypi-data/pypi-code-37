import unittest
from vndb_thigh_highs import Config, VNDB
from vndb_thigh_highs.models import Votelist
from vndb_thigh_highs.error import ResponseError, ResponseErrorId
from test_case import TestCase

class LoginTest(TestCase):
    def test_double_login(self):
        vndb = VNDB()
        vndb.login()
        vndb.logout()
        vndb.login()
        vndb.logout()

    @unittest.skip("""Testing too many times causes the server to
    refuse future login. Enable once in a while.""")
    def test_auth_error(self):
        config = Config()
        config.login.username = "foiegras"
        config.login.password = "not_foiegras_password"
        vndb = VNDB(config=config)
        try:
            vndb.login()
            self.assertTrue(False)
        except ResponseError as e:
            self.assertEqual(e.id, ResponseErrorId.AUTH)
        finally:
            vndb.logout()

    def test_already_loged_in_error(self):
        vndb = VNDB()
        vndb.login()
        try:
            vndb.login()
            self.assertTrue(False)
        except ResponseError as e:
            self.assertEqual(e.id, ResponseErrorId.LOGGED_IN)
        finally:
            vndb.logout()

    def test_need_login_error(self):
        vn_id = 17
        new_vote = 100
        vndb = VNDB()
        try:
            vndb.set_votelist(vn_id, {Votelist.vote: new_vote})
            self.assertTrue(False)
        except ResponseError as e:
            self.assertEqual(e.id, ResponseErrorId.NEED_LOGIN)
        finally:
            vndb.logout()
