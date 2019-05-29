import pandas as pd


class ForecastClassificator(object):
    def __init__(self, high_sell_classification_model, known_products):
        self.high_sell_classification_model = high_sell_classification_model
        self.known_products = known_products

    def classify(self, data: pd.DataFrame):
        data["KNOWN"] = data[data["PROD_ID"] in self.known_products]
        data["HIGH_SELL"] = self.high_sell_classification_model.predict(data)

        data["CLASSIFICATION"] =  data["KNOWN", "HIGH_SELL"].apply(ForecastClassificator.get_classification)

    @staticmethod
    def get_classification(is_known: bool, is_high_sell: bool):
        if is_high_sell and is_known:
            return "high_known"
        if not is_high_sell and is_known:
            return "low_known"
        if is_high_sell and not is_known:
            return "high_unknown"
        if not is_high_sell and not is_known:
            return "low_unknown"

        return "unknown"
