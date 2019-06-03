import unittest
import os
import pandas as pd
from .cleaning import *

class TestAddBadIndicator(unittest.TestCase):
    def setUp(self):
        dirname = os.path.dirname(__file__)
        self.dataset = pd.read_csv(dirname + "/resources/train.csv")

    def test_raises_errors_for_column_overwrite(self):
        self.dataset["Cabin_is_bad"] = 9

        self.assertRaises(AssertionError, add_bad_indicator_vars, self.dataset)

    def test_raises_adds_bad_value_columns(self):
        self.assertEqual(12, len(self.dataset.columns))
        add_bad_indicator_vars(self.dataset)

        self.assertEqual(15, len(self.dataset.columns))
        self.assertEqual(687, self.dataset["Cabin_is_bad"].sum())
        self.assertEqual(2, self.dataset["Embarked_is_bad"].sum())
        self.assertEqual(177, self.dataset["Age_is_bad"].sum())

class TestColumnReplace(unittest.TestCase):
    def setUp(self):
        dirname = os.path.dirname(__file__)
        self.dataset = pd.read_csv(dirname + "/resources/train.csv")
        self.houses = pd.read_csv(dirname + "/resources/houses_train.csv")
    
    def test_raises_adds_bad_value_columns(self):
        self.assertEqual(3, self.dataset.isna().any().sum())
        self.assertEqual(25, (self.dataset["Age"] == 28.0).sum())
        self.assertEqual(687, self.dataset["Cabin"].isna().sum())
        self.assertEqual(2, self.dataset["Embarked"].isna().sum())

        replace_bad_values_with_median(self.dataset)
        self.assertEqual(0, self.dataset.isna().any().sum())
        self.assertEqual(202, (self.dataset["Age"] == 28.0).sum())
        self.assertEqual(687, (self.dataset["Cabin"] == "unknown").sum())
        self.assertEqual(2, (self.dataset["Embarked"] == "unknown").sum())

    def test_raises_adds_bad_value_columns_for_house_data(self):
        self.assertEqual(19, self.houses.isna().any().sum())

        replace_bad_values_with_median(self.houses)
        self.assertEqual(0, self.houses.isna().any().sum())

    def test_raises_adds_bad_value_columns_no_existing_unknowns(self):
        self.dataset.loc[0, "Cabin"] = "unknown"
        self.assertRaises(AssertionError, replace_bad_values_with_median, self.dataset)

class TestBasicBadValEliminate(unittest.TestCase):
    def setUp(self):
        dirname = os.path.dirname(__file__)
        self.houses = pd.read_csv(dirname + "/resources/houses_train.csv")
    
    def test_raises_adds_bad_value_columns_for_house_data(self):
        self.assertEqual(19, self.houses.isna().any().sum())
        self.assertEqual(81, len(self.houses.columns))

        remove_bad_vals_basic(self.houses)
        self.assertEqual(0, self.houses.isna().any().sum())
        self.assertEqual(100, len(self.houses.columns))

class TestCategorization(unittest.TestCase):
    def setUp(self):
        dirname = os.path.dirname(__file__)
        self.houses = pd.read_csv(dirname + "/resources/houses_train.csv")
    
    def test_converts_objects_to_categorical(self):
        self.assertEqual(43, len(self.houses.select_dtypes(include="object").columns))
        self.assertEqual(0, len(self.houses.select_dtypes(include="category").columns))

        categorize(self.houses)
        self.assertEqual(0, len(self.houses.select_dtypes(include="object").columns))
        self.assertEqual(43, len(self.houses.select_dtypes(include="category").columns))
        self.assertEqual(124, len(self.houses.columns))


    def test_raises_error_on_col_name_conflicts(self):
        self.houses["LandSlope_mapping"] = 0
        self.assertRaises(AssertionError, categorize, self.houses)
