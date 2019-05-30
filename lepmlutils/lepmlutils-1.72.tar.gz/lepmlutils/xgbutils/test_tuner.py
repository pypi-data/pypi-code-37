import unittest
import os
import pandas as pd
from .tuner import Tuner

class TestTuner(unittest.TestCase):
    def test_partitions_correctly(self):
        dirname = os.path.dirname(__file__)
        dataset = pd.read_csv(dirname + "/resources/train.csv")
        
        features = [ 
            "Age", 
            "SibSp", 
            "Parch", 
            "Fare", 
        ]
        target = [
            "Survived",
        ]
        candidates = {
            'max_depth': range(4, 40, 10),
        }
        set_params = {
            "n_estimators": 40,
        }

        tuner = Tuner()
        results = tuner.tune(
            candidates,
            set_params,
            dataset,
            features,
            target,
            3,
        )

        self.assertEqual(4, len(results))
        for params in results:
            self.assertEqual(params["params"]["n_estimators"], 40)
        
        self.assertEqual(results[0]["params"]["max_depth"], 4)
        self.assertEqual(results[1]["params"]["max_depth"], 24)
        self.assertEqual(results[2]["params"]["max_depth"], 34)
        self.assertEqual(results[3]["params"]["max_depth"], 14)

        self.assertGreaterEqual(results[0]["test_score"], results[1]["test_score"])
        self.assertGreaterEqual(results[1]["test_score"], results[2]["test_score"])
        self.assertGreaterEqual(results[2]["test_score"], results[3]["test_score"])
