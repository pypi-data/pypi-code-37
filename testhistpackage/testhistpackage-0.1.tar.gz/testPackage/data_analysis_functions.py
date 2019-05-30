import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from pandas import Series
from matplotlib import pyplot
from statsmodels.graphics.tsaplots import plot_acf
#from statsmodels.tsa import stattools
from scipy.stats import norm
from scipy import stats
import pylab
import math
from matplotlib import dates, ticker
from numpy import zeros
from mpl_finance import candlestick_ohlc

def remove_nan(df):
    df_nan = df[df.isna().any(axis=1)]
    dffilter = df.dropna()
    return df_nan,dffilter

def remove_zero(df, remove_zero_flag):
    # function remove_zero removes nan values first to detect zero values
    df_nan,dffilter = remove_nan(df)
    dffilter = dffilter.replace(0, pd.np.nan)

    dfzero = dffilter[dffilter.isna().any(axis=1)]
    dfzero = dfzero.fillna(0)

    if remove_zero_flag == 1:
        dffilter = dffilter.dropna()
    else:
        dffilter = dffilter.fillna(0)
    return dfzero, dffilter

def remove_negative(df, drop_zero_flag):
    _, dffilter = remove_zero(df, drop_zero_flag)
    dffilter_negative = np.sign(dffilter.loc[:, 'Open':'Volume'])
    dffilter_negative = dffilter_negative.replace(-1, pd.np.nan)
    dferr = dffilter[dffilter_negative.isna().any(axis=1)]

    dffilter = dffilter.assign(sgnO=dffilter_negative.loc[:, 'Open'])
    dffilter = dffilter.assign(sgnH=dffilter_negative.loc[:, 'High'])
    dffilter = dffilter.assign(sgnC=dffilter_negative.loc[:, 'Close'])
    dffilter = dffilter.assign(sgnL=dffilter_negative.loc[:, 'Low'])
    dffilter = dffilter.assign(sgnAC=dffilter_negative.loc[:, 'Adj Close'])
    dffilter = dffilter.assign(sgnV=dffilter_negative.loc[:, 'Volume'])
    # dffilter = dffilter.replace(-1, pd.np.nan)

    dffilter = dffilter.dropna()
    dffilter = dffilter.loc[:, 'Date':'Volume']

    return dferr, dffilter




def remove_HO_CL_error(df, drop_zero_flag):
    _, dffilter = remove_negative(df, drop_zero_flag)
    OHError = np.sign(dffilter.High - dffilter.Open)
    CLError = np.sign(dffilter.Close - dffilter.Low)
    LHError = np.sign(dffilter.High - dffilter.Low)
    CHError =  np.sign(dffilter.High - dffilter.Close)
    OLError = np.sign(dffilter.Open - dffilter.Low)

    # plt.subplot(1,2,1)
    # plt.tight_layout()
    # plt.plot(OHError)
    # plt.xlabel('Index')
    # plt.ylabel('OHError')
    #
    # plt.subplot(1, 2, 2)
    # plt.tight_layout()
    # plt.plot(CLError)
    # plt.xlabel('Index')
    # plt.ylabel('CLError')

    dffilter = dffilter.assign(sgnOHE=OHError)
    dffilter = dffilter.assign(sgnCLE=CLError)
    dffilter = dffilter.assign(sgnLHE=LHError)
    dffilter = dffilter.assign(sgnCHE=CHError)
    dffilter = dffilter.assign(sgnOLE=OLError)
    dffilter = dffilter.replace(-1, pd.np.nan)

    dferr = dffilter[dffilter.isna().any(axis=1)]
    dferr = dferr.fillna(-1)

    dffilter=dffilter.dropna()
    dffilter = dffilter.loc[:, 'Date':'Volume']
    return dferr, dffilter

def CandleStickPlot_fun(df, num_rows, num_cols, drop_zero_flag, dates_flag):
    dferr, dffilter = remove_HO_CL_error(df, drop_zero_flag)
    dfanalysis = dffilter
    ohlc_data = (dfanalysis.loc[:, 'Date':'Close'])

    if dates_flag == 1:
        dates_num = dates.datestr2num(dfanalysis.loc[:, 'Date'])
        ohlc_data.Date = dates_num
    else:
        ohlc_data.Date = dfanalysis.Date[dfanalysis.Date == dfanalysis.Date].index

    fig, ax = plt.subplots(nrows=num_rows, ncols=num_cols)
    window = math.ceil(np.max(ohlc_data.shape) / (num_rows * num_cols))
    ax1 = ax

    a = 0
    b = 1
    for i in range(ax.shape[0]):
        for j in range(ax.shape[1]):
            if i == ax.shape[0] and j == ax.shape[1]:
                candlestick_ohlc(ax[i, j], ohlc_data.loc[a * window:np.max(ohlc_data.shape), :].values, width=0.5,
                                 colorup='g', colordown='r', alpha=0.8)
                a += 1
                b += 1
            else:
                candlestick_ohlc(ax[i, j], ohlc_data.loc[a * window:b * window, :].values, width=0.5, colorup='g',
                                 colordown='r', alpha=0.8)
                a += 1
                b += 1

    plt.tight_layout()
    ax2 = ax
    ax3 = ax
    for ax in ax2.flat:
        ax.set(xlabel='Index', ylabel='Price: Open, High, Close, Low')

    for ax in ax3.flat:
        ax.xaxis.set_major_locator(ticker.MaxNLocator(20))

    if dates_flag == 1:
        dayFormatter = dates.DateFormatter('%d-%b-%Y')
        for ax in ax3.flat:
            ax.xaxis.set_major_formatter(dayFormatter)
    return None







    # def outlier_LinRegress(df, Xvariable, Yvariable, cutoff):
#     dferr, dffilter = remove_HO_CL_error(df)
#     Xdata = dffilter.loc[:, Xvariable]
#     Ydata = dffilter.loc[:, Yvariable]
#
#     statsXY = linregress(Xdata, Ydata)
#     SlopeXY = statsXY.slope
#     InterceptXY = statsXY.intercept
#
#     LineXY = SlopeXY * Xdata + InterceptXY
#
#     Error = Ydata - LineXY
#
#     # print(np.mean(Error))
#     sigmaE = np.std(Error)
#     len = max(Ydata.shape)
#
#     UC = LineXY + cutoff * sigmaE * np.repeat(1, len)
#     LC = LineXY - cutoff * sigmaE * np.repeat(1, len)
#
#     OLA = np.sign(UC - Ydata)
#     OLB = np.sign(Ydata - LC)
#
#     dffilter = dffilter.assign(sgnOLA=OLA)
#     dffilter = dffilter.assign(sgnOLB=OLB)
#
#     dffilter = dffilter.replace(-1, pd.np.nan)
#     dfOL = dffilter[dffilter.isna().any(axis=1)]
#     dfOL = dfOL.fillna(-1)
#
#     # print(dfOL.loc[:,'Date':'Volume'])
#
#     OLXdata = dfOL.loc[:, Xvariable]
#     OLYdata = dfOL.loc[:, Yvariable]
#
#     plt.figure(figsize=(20, 10))
#     plt.subplot(1, 3, 1)
#     plt.plot(Xdata, Ydata, 'b .',
#              Xdata, LineXY, 'm',
#              Xdata, UC, 'g-',
#              OLXdata, OLYdata, 'r .')
#     plt.gca().legend(('Data: ' + Xvariable + ', ' + Yvariable, 'Regression line', 'Confidence Bands', 'Outliers'))
#     plt.plot(Xdata, LC, 'g-')
#     plt.xlabel(Xvariable)
#     plt.ylabel(Yvariable)
#
#     plt.subplot(1, 3, 2)
#     plt.hist(Error, bins=np.max(Error.shape), density=True)
#     plt.xlabel('Error in regression')
#     plt.ylabel('Frequency')
#
#     plt.subplot(1, 3, 3)
#     plt.plot(Ydata, 'b', OLYdata, 'r .')
#     plt.gca().legend((Yvariable, 'Outliers'))
#     plt.xlabel('Index')
#     plt.ylabel(Yvariable)
#     plt.tight_layout()
#     return dfOL.loc[:,'Date':'Volume']


def outlier_LinRegress(df, Yvariable, cutoff, corr_mat, drop_zero_flag):
    s = pd.Series(data=np.zeros([1, corr_mat.shape[0]])[0], index=list(corr_mat.columns))
    np.fill_diagonal(corr_mat.values, s)

    a = corr_mat.loc[:, Yvariable]
    b = np.max(corr_mat.loc[:, Yvariable])
    Xvariable = a[a == b].index[0]
    dferr, dffilter = remove_HO_CL_error(df, drop_zero_flag)
    Xdata = dffilter.loc[:, Xvariable]
    Ydata = dffilter.loc[:, Yvariable]

    statsXY = linregress(Xdata, Ydata)
    SlopeXY = statsXY.slope
    InterceptXY = statsXY.intercept

    LineXY = SlopeXY * Xdata + InterceptXY

    Error = Ydata - LineXY

    # print(np.mean(Error))
    sigmaE = np.std(Error)
    len = max(Ydata.shape)

    UC = LineXY + cutoff * sigmaE * np.repeat(1, len)
    LC = LineXY - cutoff * sigmaE * np.repeat(1, len)

    OLA = np.sign(UC - Ydata)
    OLB = np.sign(Ydata - LC)

    dffilter = dffilter.assign(sgnOLA=OLA)
    dffilter = dffilter.assign(sgnOLB=OLB)

    dffilter = dffilter.replace(-1, pd.np.nan)
    dfOL = dffilter[dffilter.isna().any(axis=1)]
    dfOL = dfOL.fillna(-1)

    # print(dfOL.loc[:,'Date':'Volume'])

    OLXdata = dfOL.loc[:, Xvariable]
    OLYdata = dfOL.loc[:, Yvariable]

    plt.figure(figsize=(20, 10))
    plt.subplot(1, 2, 1)
    plt.plot(Xdata, Ydata, 'b .',
             Xdata, LineXY, 'm',
             Xdata, UC, 'g-',
             OLXdata, OLYdata, 'r .')
    plt.gca().legend(('Data: ' + Xvariable + ', ' + Yvariable, 'Regression line', 'Confidence Bands', 'Outliers'))
    plt.plot(Xdata, LC, 'g-')
    plt.xlabel(Xvariable)
    plt.ylabel(Yvariable)

    # plt.subplot(1, 3, 2)
    # plt.hist(Error, bins=np.max(Error.shape), density=True)
    # plt.xlabel('Error in regression')
    # plt.ylabel('Frequency')

    plt.subplot(1, 2, 2)
    plt.plot(Ydata, 'b', OLYdata, 'r .')
    plt.gca().legend((Yvariable, 'Outliers'))
    plt.xlabel('Index')
    plt.ylabel(Yvariable)
    plt.tight_layout()
    return dfOL.loc[:,'Date':'Volume']