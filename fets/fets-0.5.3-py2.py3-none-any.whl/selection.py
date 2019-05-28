from sklearn.base import TransformerMixin


class DFColumSelect(TransformerMixin):

    def __init__(self, key=None):
        """ Initializes the column key name

            :param key: column name
        """
        self.key = ""
        if key is not None:
            self.key = str(key)

    def fit(self, x, y=None):
        return self

    def transform(self, input_df):
        """ It will return the selected column or the first column
        
            :param input_df: input dataframe on which a column will be selected.
        """
        if self.key in input_df.columns:
            return input_df[self.key]
        # returning first column if no choices expressed
        return input_df[input_df.columns[0]]

