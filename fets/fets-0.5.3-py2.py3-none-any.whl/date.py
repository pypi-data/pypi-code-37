from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class TSNumericalToDate(BaseEstimator, TransformerMixin):
    """ Transforms a non-Unix time in the numerical form YYYYMMDD(.0) or any
    lower values for month or year resolution into a timestamp object. It also
    contains the dates in given limits when given.

    """
    def __init__(self, past_limit=None, future_limit=None, fill_date=None):
        """ Initialize user defined date limits

           :param past_limit: string for an ISO date to bound the past, or
           anything datetime() can handle

           :param future_limit: string for an ISO date to bound the future, or
           anything datetime() can handle

           :param fill_date: datetime object to fill missing dates
        """
        self.past_limit = None
        self.future_limit = None
        self.fill_date = datetime(1800, 1, 1)

        # User wanted to have some limits, let the exceptions raise.
        if not (isinstance(past_limit, datetime) or past_limit is None):
            raise TypeError("Input parameter is not a datetime: past_limit")
        if not (isinstance(future_limit, datetime) or future_limit is None):
            raise TypeError("Input parameter is not a datetime: future_limit")
        if not (isinstance(fill_date, datetime) or fill_date is None):
            raise TypeError("Input parameter is not a datetime: fill_date")

        if past_limit is not None:
            self.past_limit = past_limit
        if future_limit is not None:
            self.future_limit = future_limit
        if fill_date is not None:
            self.fill_date = fill_date

    def apply_day_resolution(self, input_s):
        """ Replace numerical dates by full resolution date numbers

            201501 is at the month resolution and will be completed to
            20150101 (with first day of the month)

            :param input_s: input series
            :return: day resolution series without
        """
        # --- Replace numbers on non null data only
        in_dates = input_s.dropna()
        # Transforms a year only to day resolution on first of january
        year_res = in_dates[(in_dates >= 1e3) & (in_dates < 1e4)].apply(lambda x: x*10000+101)
        # Transforms a month resolution date to day resolution on first of the given month
        month_res = in_dates[(in_dates >= 1e5) & (in_dates < 1e6)].apply(lambda x: x*100+1)
        # Keep day resolution dates as is
        day_res = in_dates[(in_dates >= 1e7) & (in_dates < 1e8)]

        # --- Return only valid data
        return day_res.combine_first(month_res).combine_first(year_res)

    def fit(self, X, y=None):
        return self

    def transform(self, input_s):
        """ Transform input numerical series into pandas datetime

        """
        if not isinstance(input_s, pd.Series):
            raise TypeError("requires pandas Series as input")

        # --- get day resolution, nan won't be in the list.
        day_dates = self.apply_day_resolution(input_s)

        def my_datetime(x):
            year = int(x/10000)
            month = int((x-year*10000)/100)
            day = int(x-(year*10000+month*100))
            return datetime(year, month, day)

        # --- Converts to datetime with errors=coerce to have NaT when appropriate
        tr_dates = day_dates.apply(lambda x: my_datetime(x))

        # --- Reindex and Invalidate all other dates
        if self.past_limit is not None:
            tr_dates[tr_dates < self.past_limit] = self.past_limit

        if self.future_limit is not None:
            tr_dates[tr_dates> self.future_limit] = self.future_limit

        all_dates = tr_dates.reindex(input_s.index,
                                     method=None,
                                     fill_value=self.fill_date)
        return all_dates
