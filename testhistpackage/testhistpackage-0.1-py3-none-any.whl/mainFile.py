import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from pandas import Series
from matplotlib import pyplot
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa import stattools
from scipy.stats import norm
from scipy import stats
import pylab
import math
from matplotlib import dates, ticker
from numpy import zeros
from mpl_finance import candlestick_ohlc
from .data_analysis_functions import remove_nan, remove_zero, remove_HO_CL_error, outlier_LinRegress

def mainFun(a,b):
    missing_values = ["null", "NuLL", "NULL", "Null", 'NAN', 'NaN', 'nan', "--"]
    df = pd.read_csv(a,na_values=missing_values)
    corr_mat = df.corr()
    #print(corr_mat)
    drop_zero_flag = 1
    df_Outlier_Open = outlier_LinRegress(df.loc[:, 'Date':'Volume'], 'Open', 5, corr_mat, drop_zero_flag)
    #print(df_Outlier_Open)
    output_file = df_Outlier_Open
    output_file.to_csv(b)
    return 'done'