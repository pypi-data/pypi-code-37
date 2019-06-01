import unittest
from ybc_music import *


class MyTestCase(unittest.TestCase):
    def test_search_music(self):
        self.assertIsNotNone(search_music('结果', '花儿乐队'))

    def test_search_music_typeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用search_music方法时，'name'参数类型错误。$"):
            search_music(123, "花儿乐队")
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用search_music方法时，'ar'参数类型错误。$"):
            search_music("花火", 123)

        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用search_music方法时，'name'、'ar'参数类型错误。$"):
            search_music(123, 123)

    def test_search_music_valueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用search_music方法时，'name'参数不在允许范围内。$"):
            search_music("", '花儿乐队')
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用search_music方法时，'ar'参数不在允许范围内。$"):
            search_music("花火", "")


if __name__ == '__main__':
    unittest.main()
