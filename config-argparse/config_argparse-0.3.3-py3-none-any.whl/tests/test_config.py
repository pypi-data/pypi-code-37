import unittest
import argparse
from collections import namedtuple
from config_argparse import Config, DynamicConfig, Value


class TestConfig(unittest.TestCase):
    def test_basic(self):
        class C(Config):
            str = 'test'
            int = 1
            float = 1.0
            bool = False

        c = C()
        self.assertEqual(c.str, 'test')
        self.assertEqual(c.int, 1)
        self.assertEqual(c.float, 1.0)
        self.assertEqual(c.bool, False)

    def test_nest(self):
        class C1(Config):
            c1 = 1

        class C2(Config):
            c2 = 2

        class C3(Config):
            c3 = 3
            c1 = C1()

        class C4(C1, C2):
            c4 = DynamicConfig(lambda x: C3())

        class C5(C1, C2):
            c5 = DynamicConfig(lambda x: C3(), auto_load=True)

        self.assertEqual(C3().c1.c1, 1)
        c = C4()
        self.assertEqual(c.c1, 1)
        self.assertEqual(c.c2, 2)
        self.assertEqual(c.c4, None)
        self.assertEqual(C5().c5.c3, 3)
        self.assertEqual(C5().c5.c1.c1, 1)

    def test_multi_dynamic(self):
        class C1(Config):
            c1 = 1

        class C2(Config):
            c2 = DynamicConfig(lambda x: [C1(), C1(), C1()], auto_load=True)

        self.assertEqual(C2().c2, [C1(), C1(), C1()])

    def test_dynamic_none(self):
        class C2(Config):
            c2 = DynamicConfig(lambda x: None, auto_load=True)

        self.assertEqual(C2().c2, None)

    def test_parse_args(self):
        class C(Config):
            a = 1

        c = C()
        cc = c.parse_args([])
        self.assertEqual(cc.a, 1, 'default value')
        cc = c.parse_args(['--a', '10'], namespace=cc)
        self.assertEqual(cc.a, 10, 'update works')
        cc = c.parse_args(['--a', '100'], namespace=cc)
        self.assertEqual(cc.a, 100, 'update multiple times works')

    def test_parse_basic_types(self):
        class C(Config):
            str = 'test'
            int = 1
            float = 1.0
            bool = False

        c = C()
        cc = c.parse_args(['--str', 'foo', '--int', '10', '--float', '10.5', '--bool'])
        self.assertEqual(cc.str, 'foo', 'str')
        self.assertEqual(cc.int, 10, 'int')
        self.assertEqual(cc.float, 10.5, 'float')
        self.assertEqual(cc.bool, True, 'bool')

    def test_parse_list(self):
        class C(Config):
            a = [1, 2, 3]

        c = C()
        cc = c.parse_args([])
        self.assertEqual(cc.a, [1, 2, 3], 'default value')
        cc = c.parse_args(['--a', '1', '3', '5'], namespace=cc)
        self.assertEqual(cc.a, [1, 3, 5], 'update works')

    def test_parse_nested(self):
        class Nest(Config):
            a = 1

        class C(Config):
            a = 0.1
            nest = Nest()

        c = C()
        cc = c.parse_args([])
        self.assertEqual(cc.a, 0.1, 'default value')
        self.assertEqual(cc.nest.a, 1, 'default value in nest')
        cc = c.parse_args(['--nest.a', '10'], namespace=cc)
        self.assertEqual(cc.a, 0.1, 'should not be overwritten')
        self.assertEqual(cc.nest.a, 10, 'should be overwritten')

    def test_parse_nested_nested(self):
        class NestNest(Config):
            a = 'str'

        class Nest(Config):
            a = 1
            nest = NestNest()

        class C(Config):
            a = 0.1
            nest = Nest()

        c = C()
        cc = c.parse_args([])
        self.assertEqual(cc.a, 0.1, 'default value')
        self.assertEqual(cc.nest.a, 1, 'default value in nest')
        self.assertEqual(cc.nest.nest.a, 'str', 'default value in nest in nest')

        cc = c.parse_args(['--nest.nest.a', '10'], namespace=cc)
        self.assertEqual(cc.a, 0.1, 'should not be overwritten')
        self.assertEqual(cc.nest.a, 1, 'should not be overwritten')
        self.assertEqual(cc.nest.nest.a, '10', 'should be overwritten')

    def test_unknown_args(self):
        class Nest(Config):
            a = 0

        class C(Config):
            a = 0
            nest = Nest()

        c = C()
        with self.assertRaises(Exception):
            c.parse_args(['--unknown', '10'])

        with self.assertRaises(Exception):
            c.parse_args(['--nest.b', '10'])

    def test_parse_dynamic(self):
        class NestA(Config):
            a = 'str'

        class NestB(Config):
            b = 1

        class C(Config):
            a = 0.1
            nest = 'a'
            nest_cfg = DynamicConfig(lambda c: NestA() if c.nest == 'a' else NestB())

        c = C()
        cc = c.parse_args([])

        self.assertTrue(isinstance(cc.nest_cfg, NestA), 'nest_cfg should be NestA, but {}'.format(type(cc.nest_cfg)))
        self.assertEqual(cc.nest_cfg.a, 'str')

        cc = c.parse_args(['--nest', 'b'])
        self.assertTrue(isinstance(cc.nest_cfg, NestB), 'nest_cfg should be NestB, but {}'.format(type(cc.nest_cfg)))
        self.assertFalse(hasattr(cc.nest_cfg, 'a'))
        self.assertEqual(cc.nest_cfg.b, 1)

        cc = c.parse_args(['--nest', 'b', '--nest_cfg.b', '100'])
        self.assertTrue(isinstance(cc.nest_cfg, NestB))

        self.assertEqual(cc.nest_cfg.b, 100)

    def test_unknown_dynamic_args(self):
        class NestA(Config):
            a = 'str'

        class NestB(Config):
            b = 1

        class C(Config):
            a = 0.1
            nest = 'a'
            nest_cfg = DynamicConfig(lambda c: NestA() if c.nest == 'a' else NestB())

        c = C()
        with self.assertRaises(Exception):
            c.parse_args(['--nest', 'a', '--nest_cfg.b', '10'])

        with self.assertRaises(Exception):
            c.parse_args(['--nest', 'b', '--nest_cfg.a', '10'])

    def test_inherit(self):
        class CC1(Config):
            a = 0.1

        class CC2(Config):
            b = 'str'

        class C(CC1, CC2):
            c = 1

        c = C()
        cc = c.parse_args([])
        self.assertEqual(cc.a, 0.1)
        self.assertEqual(cc.b, 'str')
        self.assertEqual(cc.c, 1)

        cc = c.parse_args(['--a', '0.2', '--b', 'foo', '--c', '2'])
        self.assertEqual(cc.a, 0.2)
        self.assertEqual(cc.b, 'foo')
        self.assertEqual(cc.c, 2)

    def test_inherit_overwrite(self):
        class CC1(Config):
            a = 0.1

        class C(CC1):
            a = 'str'

        c = C()
        cc = c.parse_args([])
        self.assertEqual(cc.a, 'str')

        cc = c.parse_args(['--a', 'foo'])
        self.assertEqual(cc.a, 'foo')

    def test_value(self):
        class C(Config):
            a = Value(10)
            b = Value('str')
            c = Value(1.0)
            d = Value([1, 2, 3])

        c = C()
        cc = c.parse_args([])

        self.assertEqual(cc.a, 10)
        self.assertEqual(cc.b, 'str')
        self.assertEqual(cc.c, 1.0)
        self.assertEqual(cc.d, [1, 2, 3])

        cc = c.parse_args(['--a', '100'])
        self.assertEqual(cc.a, 100)

    def test_value_required(self):
        class C(Config):
            a = Value(type=int, required=True)

        c = C()
        with self.assertRaises(SystemExit):
            cc = c.parse_args(['--b', 'a'])

    def test_value_choices(self):
        class C(Config):
            a = Value(type=int, choices=[1, 2])

        c = C()
        with self.assertRaises(SystemExit):
            cc = c.parse_args(['--a', '10'])
        cc = c.parse_args(['--a', '2'])
        self.assertEqual(cc.a, 2)

    def test_assign_defaults(self):
        class C(Config):
            a = 100

        default = {'a': 1}

        c = C(default)
        cc = c.parse_args([])
        self.assertEqual(cc.a, 1)

        with self.assertRaises(KeyError):
            C({'b': 1})

    def test_assign_defaults_nested(self):
        class C2(Config):
            a = 100

        class C(Config):
            a = 100
            c = C2()

        default = {'a': 1, 'c': {'a': 2}}

        c = C(default)
        cc = c.parse_args([])
        self.assertEqual(cc.a, 1)
        self.assertEqual(cc.c.a, 2)

        default = {'a': 1, 'c': 2}
        with self.assertRaises(Exception):
            c = C(default)

    def test_assign_defaults_dynamic(self):
        class C2(Config):
            b = 10

        class C(Config):
            a = DynamicConfig(lambda x: C2())

        self.assertEqual(C({'a': {'b': 100}}).parse_args([]).a.b, 100)

    def test_assign_defaults_multi_dynamic(self):
        class C2(Config):
            b = 10

        class C(Config):
            a = DynamicConfig(lambda x: [C2(), C2()], auto_load=True)

        c = C({'a': [{'b': 100}, {'b': 99}]}).parse_args([])
        self.assertEqual(c.a[0].b, 100)
        self.assertEqual(c.a[1].b, 99)

    def test_compare(self):
        class C2(Config):
            a = 200

        class C(Config):
            a = 100
            c = C2()

        c = C()
        cc1 = c.parse_args(['--c.a', '1'])
        cc2 = c.parse_args(['--c.a', '1'])
        c = C()
        cc3 = c.parse_args(['--c.a', '1'])
        c = C()
        cc4 = c.parse_args(['--c.a', '2'])
        self.assertEqual(cc1, cc2)
        self.assertEqual(cc2, cc3)
        self.assertNotEqual(cc4, cc1)
        self.assertNotEqual(cc4, cc2)
        self.assertNotEqual(cc4, cc3)

    def test_todict(self):
        import json

        class C2(Config):
            a = 100

        class C(Config):
            a = 100
            c = C2()
            c3 = Value(100)

        c = C()
        cc = c.parse_args(['--c.a', '1'])
        c2 = C(json.loads(json.dumps(cc.todict())))
        cc2 = c.parse_args(['--c.a', '1'])
        self.assertEqual(cc, cc2)

    def test_dynamic_todict(self):
        import json

        class C2(Config):
            a = 100

        class C(Config):
            a = DynamicConfig(lambda c: [C2(), C2(), C2()])

        c = C().parse_args()
        c2 = C(json.loads(json.dumps(c.todict()))).parse_args()
        self.assertEqual(c, c2)


if __name__ == "__main__":
    unittest.main()