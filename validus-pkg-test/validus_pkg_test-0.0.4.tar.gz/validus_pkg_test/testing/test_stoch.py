import unittest
from validus_pkg_test.SV_MC import stochastic_volatility_run
 
class TestUM(unittest.TestCase):

    def setUp(self):
        pass
 
    def test_stoch_run_1(self):
        self.assertEqual( stochastic_volatility_run(1,1,1,1,0,1), 1.)
 
    def test_stoch_run_0(self):
        self.assertEqual(stochastic_volatility_run(1,1,1,1,0,0), 0.)
 
if __name__ == '__main__':
    unittest.main()