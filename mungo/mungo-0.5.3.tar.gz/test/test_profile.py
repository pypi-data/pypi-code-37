import sys
import unittest
from unittest.mock import patch

from mungo.cli import main


class TestPackageSplitting(unittest.TestCase):

    def test_profile_install(self):
        with patch.object(sys, 'argv', ["mungo", "install", "keras", "python>=3.7", "--offline", "--dag"]):
            print(sys.argv)
            main()


if __name__ == '__main__':
    unittest.main()
