import pandas as pd
from .api_call import api_call
from .metadata_old import metadata_old

def timeseries(series, groupby=None, year=None, yearGreaterThan=None, yearSmallerThan=None, day=None, dayGreaterThan=None, daySmallerThan=None, month=None, monthGreaterThan=None, monthSmallerThan=None, code=None, date=None):
    """Returns the specified time series' data values. `series` must be a time series code."""
    if groupby is not None:
        df = get_nivel_region(series)
        if df['NIVNOME'].isin([groupby]).any():
            api = ("http://ipeadata2-homologa.ipea.gov.br/api/v1/AnoValors"
                   "(SERCODIGO='{}',NIVNOME='{}')?$top=100&$skip=0&$orderby"
                   "=SERATUALIZACAO&$count=true").format(series, groupby)
            return api_call(api)
        return None
    api = "http://ipeadata2-homologa.ipea.gov.br/api/v1/ValoresSerie(SERCODIGO='%s')" % series
    
    if list(metadata_old(series)['BIG THEME']) == ['Regional']:
        ts_df = api_call(api).rename(index=str, columns={"SERCODIGO": "CODE", "VALDATA": "DATE", "VALVALOR": "VALUE ("+list(metadata_old(series)['MEASURE'])[0]+")"})
    else: 
        ts_df = api_call(api)[['ANO','DIA','MES','SERCODIGO','VALDATA','VALVALOR']].rename(index=str, columns={"ANO": "YEAR", "DIA": "DAY", "MES": "MONTH", "SERCODIGO": "CODE", "VALDATA": "DATE", "VALVALOR": "VALUE ("+list(metadata_old(series)['MEASURE'])[0]+")"})
        #api_call(api).rename(index=str, columns={"SERCODIGO": "CODIGO", "VALDATA": "DATA", "VALVALOR": "VALOR ("+list(metadata_old(series)['UNINOME'])[0]+")"})
    if year is not None:
        ts_df = ts_df.loc[ts_df["YEAR"] == year]
    if yearGreaterThan is not None:
        ts_df = ts_df.loc[ts_df["YEAR"] > yearGreaterThan]
    if yearSmallerThan is not None:
        ts_df = ts_df.loc[ts_df["YEAR"] < yearSmallerThan]
    if day is not None:
        ts_df = ts_df.loc[ts_df["DAY"] == day]
    if dayGreaterThan is not None:
        ts_df = ts_df.loc[ts_df["DAY"] > dayGreaterThan]
    if daySmallerThan is not None:
        ts_df = ts_df.loc[ts_df["DAY"] < daySmallerThan]
    if month is not None:
        ts_df = ts_df.loc[ts_df["MONTH"] == month]
    if monthGreaterThan is not None:
        ts_df = ts_df.loc[ts_df["MONTH"] > monthGreaterThan]
    if monthSmallerThan is not None:
        ts_df = ts_df.loc[ts_df["MONTH"] < monthSmallerThan]
    if code is not None:
        ts_df = ts_df.loc[ts_df["CODE"] == code]
    if date is not None:
        ts_df = ts_df.loc[ts_df["DATE"] == date]
    
    return ts_df

