import unittest
import argparse
from collections import namedtuple
from config_argparse import Config, DynamicConfig, Value


class TestConfig(unittest.TestCase):
    def test1(self):
        f = None

        class MainConfig(Config):
            subs = ['a', 'b', 'c']
            sub_configs = DynamicConfig(lambda c: f(c))

        class SubConfig(Config):
            h_dims = [200]

        main = MainConfig()
        self.assertEqual(main.subs, ['a', 'b', 'c'])
        self.assertEqual(main.sub_configs, None)

        main = MainConfig({'subs': ['x', 'y']})
        self.assertEqual(main.subs, ['x', 'y'])
        self.assertEqual(main.sub_configs, None)

        def fun(c):
            self.assertEqual(c.subs, ['x', 'y'])
            self.assertEqual(c.sub_configs, None)
            return SubConfig()

        f = fun

        main = main.parse_args()
        self.assertEqual(main.subs, ['x', 'y'])

    def test2(self):
        f = None
        g = None

        class SubSubConfig(Config):
            h_dims = [200]

        class SubConfig(Config):
            subs = ['1', '2']
            sub_configs = DynamicConfig(lambda c: f(c))

        class MainConfig(Config):
            subs = ['a', 'b', 'c']
            sub_configs = DynamicConfig(lambda c: [SubConfig() for _ in range(len(c))])

        main = MainConfig({
            'subs': ['x', 'y'],
            'sub_configs': [
                {
                    'subs': ['2', '3'],
                },
                {
                    'subs': ['2', '3'],
                },
            ],
        })

        self.assertEqual(main.subs, ['x', 'y'])
        self.assertEqual(main.sub_configs, None)

        def fun(c):
            self.assertEqual(c.subs, ['2', '3'])
            self.assertEqual(c.sub_configs, None)
            return SubSubConfig()

        f = fun

        main = main.parse_args()\


if __name__ == "__main__":
    unittest.main()