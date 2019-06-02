import os
import json
import unittest
from context import abspath
from vndb_thigh_highs import VNDB
from vndb_thigh_highs import Config

LOGIN_PATH = abspath('../data/login.json')

class TestCase(unittest.TestCase):
    pass

class VNDBTestCase(TestCase):
    def setUp(self):
        self.vndb = VNDB()

    def tearDown(self):
        self.vndb.logout()

@unittest.skipUnless(os.path.isfile(LOGIN_PATH), "Missing data")
class LoggedInTestCase(VNDBTestCase):
    def setUp(self):
        with open(LOGIN_PATH) as login_file:
            data = json.load(login_file)
        config = Config()
        config.login.username = data['username']
        config.login.password = data['password']
        if config.login.password is None:
            raise unittest.SkipTest("Password not set")
        self.vndb = VNDB(config=config)
