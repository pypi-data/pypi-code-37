import pandas as pd


class MfDataFrame(pd.DataFrame):

    @property
    def _constructor(self):
        return MfDataFrame

    @staticmethod
    def speak():
        print("hey lulu it's max. We can have our own customisable data frames")
