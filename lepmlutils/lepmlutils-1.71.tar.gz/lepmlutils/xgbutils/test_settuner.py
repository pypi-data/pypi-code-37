import os
import unittest
import pandas as pd
from .settuner import SetTuner

def simple_preprocess(dataset):
    dataset["Sex"] = dataset["Sex"].replace({
        "male": 0,
        "female": 1,
    })
    
    dataset["Embarked"] = dataset["Embarked"].replace({
        "S": 0,
        "C": 1,
        "Q": 2,
        float('NaN'): 3
    })
    
    dataset["Age"].fillna(0, inplace=True)
    dataset["Fare"].fillna(0, inplace=True)    

class TestSetTuner(unittest.TestCase):
    def testEmptyTuner(self):
        tuner: SetTuner = SetTuner()
        self.assertRaises(ValueError, tuner.tune, {}, {}, None, None, None, None, True)
        self.assertRaises(RuntimeError, tuner.best_params)
        self.assertRaises(RuntimeError, tuner.best_n_params, 0)

    def testTunesCorrectly(self):
        dirname = os.path.dirname(__file__)

        train = pd.read_csv(dirname + "/resources/train.csv")
        simple_preprocess(train)
        four_fifths = 740
        teach = train[:four_fifths]
        valid = train[four_fifths:]
        features = [
            "Pclass", 
            "Sex", 
            "Age", 
            "SibSp", 
            "Parch", 
            "Fare", 
            "Embarked"
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

        tuner: SetTuner = SetTuner()

        results = tuner.tune(
            candidates, 
            set_params, 
            teach[features],
            teach[target].values.ravel(),
            valid[features],
            valid[target],
            True,
        )

        self.assertEqual(4, len(results))
        self.assertEqual(2, len(tuner.best_n_params(2)))
        self.assertEqual(3, len(tuner.best_n_params(3)))
        self.assertDictEqual(results[0], tuner.best_params())
        for params in results:
            self.assertEqual(params["params"]["n_estimators"], 40)
        
        self.assertEqual(results[0]["params"]["max_depth"], 4)
        self.assertEqual(results[1]["params"]["max_depth"], 14)
        self.assertEqual(results[2]["params"]["max_depth"], 24)
        self.assertEqual(results[3]["params"]["max_depth"], 34)





