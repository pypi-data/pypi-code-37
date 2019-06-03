import pandas as pd
import numpy as np

# for every column in the dataframe with at least 1 bad value
# another column is created with 1's for all entities with
# bad values in the original column.
def add_bad_indicator_vars(df: pd.DataFrame):
    df.apply(process_col, args=(df,))

def process_col(col: pd.Series, df: pd.DataFrame):
    pass
    if col.isna().any():
        bad_col_name = col.name + "_is_bad"
        assert(bad_col_name not in df)

        df[bad_col_name] = 0
        df.loc[df[col.name].isna(), bad_col_name] = 1

def replace_bad_values_with_median(df: pd.DataFrame):
        df.apply(replace_bad_col_values_with_median, args=(df,))

def replace_bad_col_values_with_median(col: pd.Series, df:pd.DataFrame):
    if col.isna().any():
        try:
                df[col.name] = col.fillna(col.median())
        except TypeError: 
                assert "unknown" not in col.values
                df[col.name] = col.fillna("unknown")

def remove_bad_vals_basic(df: pd.DataFrame):
        add_bad_indicator_vars(df)
        replace_bad_values_with_median(df)