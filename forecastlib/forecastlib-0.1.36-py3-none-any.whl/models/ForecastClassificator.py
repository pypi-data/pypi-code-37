import pandas as pd
import numpy as np

class ForecastClassificator(object):
    def __init__(self, high_sell_classification_model, known_products):
        self.high_sell_classification_model = high_sell_classification_model
        self.known_products = known_products

    def classify(self, data: pd.DataFrame):
        data["HIGH_SELL"] = self.high_sell_classification_model.predict(data)
        data["KNOWN"] = data["PROD_ID"].apply(lambda x: 1 if int(x) in self.known_products else 0)


        data["CLASSIFICATION"] = data.apply(lambda x: ForecastClassificator.text(x))

    @staticmethod
    def get_classification(is_known, is_high_sell):
        if is_high_sell > 0 and is_known > 0:
            return "high_known"
        if not is_high_sell == 0 and is_known > 0:
            return "low_known"
        if is_high_sell > 0 and not is_known == 0:
            return "high_unknown"
        if not is_high_sell == 0 and not is_known == 0:
            return "low_unknown"

        return "unknown"

    @staticmethod
    def test(x):
        print(x)