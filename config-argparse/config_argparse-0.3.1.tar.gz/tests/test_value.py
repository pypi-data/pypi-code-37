import unittest
import argparse
from collections import namedtuple
from config_argparse.value import Value, InferTypeError


class TestValue(unittest.TestCase):
    def test_type_inference_basic(self):
        for default, a_type, string in [
            (1, int, '1'),
            (1.0, float, '1.0'),
            ('str', str, 'str'),
            (3 + 1j, complex, '3+1j'),
        ]:

            def check(default):
                with self.subTest(msg='default = {}'.format(default)):
                    self.assertEqual(Value(default).type, a_type)

            check(default)
            check([default])
            check([default, default])
            check((default, ))
            check((default, default))

    def test_type_inference_none(self):
        with self.assertRaises(InferTypeError):
            Value(None)
        with self.assertRaises(InferTypeError):
            Value(None, choices=[])
        self.assertEqual(Value(None, type=int).type, int)
        self.assertEqual(Value(None, choices=[1, 2]).type, int)

    def test_add_argument(self):
        for default, input, parsed in [
            (1, ['2'], 2),
            (1.0, ['2.2'], 2.2),
            ('str', ['string'], 'string'),
            (3 + 1j, ['5+2j'], 5 + 2j),
            ([1, 2], ['1'], [1]),
            ([1, 2], ['1', '5'], [1, 5]),
        ]:
            with self.subTest(msg='default = {}'.format(default)):
                val = Value(default)
                parser = argparse.ArgumentParser()
                val.add_argument(parser, '--val')
                args = parser.parse_args([])
                self.assertEqual(args.val, default)
                args = parser.parse_args(['--val'] + input)
                self.assertEqual(args.val, parsed)

    def test_bool(self):
        self.assertEqual(Value(False).type, bool, 'false')

        with self.assertRaises(ValueError):
            Value(True)


if __name__ == "__main__":
    unittest.main()