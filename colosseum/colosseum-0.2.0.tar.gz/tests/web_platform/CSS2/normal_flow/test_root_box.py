from tests.utils import W3CTestCase

class TestRootBox(W3CTestCase):
    vars().update(W3CTestCase.find_tests(__file__, 'root-box-'))

