import pandas as pd
import numpy as np
from pandas import DataFrame, Series


class TA:
    @classmethod
    def SMA(cls, ohlc: DataFrame, period: int = 41, column: str = "close") -> Series:
        """
        Simple moving average - rolling mean in pandas lingo. Also known as 'MA'.
        The simple moving average (SMA) is the most basic of the moving averages used for trading.
        """

        return pd.Series(
            ohlc[column]
            .rolling(window=period)
            .mean(),
            name="{0} period SMA".format(period),
        )

    @classmethod
    def SMM(cls, ohlc: DataFrame, period: int = 9, column: str = "close") -> Series:
        """
        Simple moving median, an alternative to moving average. SMA, when used to estimate the underlying trend in a time series,
        is susceptible to rare events such as rapid shocks or other anomalies. A more robust estimate of the trend is the simple moving median over n time periods.
        """

        return pd.Series(
            ohlc[column]
            .rolling(window=period)
            .median(),
            name="{0} period SMM".format(period),
        )

    @classmethod
    def SSMA(cls, ohlc: DataFrame, period: int = 9, column: str = "close") -> Series:
        """
        Smoothed simple moving average.

        :param ohlc: data
        :param period: range
        :param column: open/close/high/low column of the DataFrame
        :return: result Series
        """

        return pd.Series(
            ohlc[column]
            .ewm(ignore_na=False, alpha=1.0 / period, min_periods=0, adjust=True)
            .mean(),
            name="{0} period SSMA".format(period),
        )

    @classmethod
    def EMA(cls, ohlc: DataFrame, period: int = 9, column: str = "close") -> Series:
        """
        Exponential Weighted Moving Average - Like all moving average indicators, they are much better suited for trending markets.
        When the market is in a strong and sustained uptrend, the EMA indicator line will also show an uptrend and vice-versa for a down trend.
        EMAs are commonly used in conjunction with other indicators to confirm significant market moves and to gauge their validity.
        """

        return pd.Series(
            ohlc[column]
            .ewm(span=period)
            .mean(),
            name="{0} period EMA".format(period),
        )

    @classmethod
    def DEMA(cls, ohlc: DataFrame, period: int = 9, column: str = "close") -> Series:
        """
        Double Exponential Moving Average - attempts to remove the inherent lag associated to Moving Averages
         by placing more weight on recent values. The name suggests this is achieved by applying a double exponential
        smoothing which is not the case. The name double comes from the fact that the value of an EMA (Exponential Moving Average) is doubled.
        To keep it in line with the actual data and to remove the lag the value 'EMA of EMA' is subtracted from the previously doubled EMA.
        Because EMA(EMA) is used in the calculation, DEMA needs 2 * period -1 samples to start producing values in contrast to the period
        samples needed by a regular EMA
        """

        DEMA = (
            2 * cls.EMA(ohlc, period)
            - cls.EMA(ohlc, period)
            .ewm(span=period)
            .mean()
        )

        return pd.Series(DEMA, name="{0} period DEMA".format(period))

    @classmethod
    def TEMA(cls, ohlc: DataFrame, period: int = 9) -> Series:
        """
        Triple exponential moving average - attempts to remove the inherent lag associated to Moving Averages by placing more weight on recent values.
        The name suggests this is achieved by applying a triple exponential smoothing which is not the case. The name triple comes from the fact that the
        value of an EMA (Exponential Moving Average) is triple.
        To keep it in line with the actual data and to remove the lag the value 'EMA of EMA' is subtracted 3 times from the previously tripled EMA.
        Finally 'EMA of EMA of EMA' is added.
        Because EMA(EMA(EMA)) is used in the calculation, TEMA needs 3 * period - 2 samples to start producing values in contrast to the period samples
        needed by a regular EMA.
        """

        triple_ema = 3 * cls.EMA(ohlc, period)
        ema_ema_ema = (
            cls.EMA(ohlc, period)
            .ewm(ignore_na=False, span=period)
            .mean()
            .ewm(ignore_na=False, span=period)
            .mean()
        )

        TEMA = (
            triple_ema
            - 3
            * cls.EMA(ohlc, period)
            .ewm(span=period)
            .mean()
            + ema_ema_ema
        )

        return pd.Series(TEMA, name="{0} period TEMA".format(period))

    @classmethod
    def TRIMA(cls, ohlc: DataFrame, period: int = 18) -> Series:
        """
        The Triangular Moving Average (TRIMA) [also known as TMA] represents an average of prices,
        but places weight on the middle prices of the time period.
        The calculations double-smooth the data using a window width that is one-half the length of the series.
        source: https://www.thebalance.com/triangular-moving-average-tma-description-and-uses-1031203
        """

        SMA = cls.SMA(ohlc, period).rolling(window=period).sum()

        return pd.Series(SMA / period, name="{0} period TRIMA".format(period))

    @classmethod
    def TRIX(cls, ohlc: DataFrame, period: int = 15) -> Series:
        """
        The Triple Exponential Moving Average Oscillator (TRIX) by Jack Hutson is a momentum indicator that oscillates around zero.
        It displays the percentage rate of change between two triple smoothed exponential moving averages.
        To calculate TRIX we calculate triple smoothed EMA3 of n periods and then substract previous period EMA3 value
        from last EMA3 value and divide the result with yesterdays EMA3 value.
        """

        EMA1 = cls.EMA(ohlc, period)
        EMA2 = EMA1.ewm(span=period).mean()
        EMA3 = EMA2.ewm(span=period).mean()
        TRIX = (EMA3 - EMA3.diff()) / EMA3.diff()

        return pd.Series(TRIX, name="{0} period TRIX".format(period))

    @classmethod
    def LWMA(cls, ohlc: DataFrame, period: int, column: str = "close") -> Series:
        """
        Linear Weighted Moving Average
        """
        raise NotImplementedError

    @classmethod
    def VAMA(cls, ohlcv: DataFrame, period: int = 8, column: str = "close") -> Series:
        """
        Volume Adjusted Moving Average
        """

        vp = ohlcv["volume"] * ohlcv[column]
        volsum = ohlcv["volume"].rolling(window=period).mean()
        volRatio = pd.Series(vp / volsum, name="VAMA")
        cumSum = (volRatio * ohlcv[column]).rolling(window=period).sum()
        cumDiv = volRatio.rolling(window=period).sum()

        return pd.Series(cumSum / cumDiv, name="{0} period VAMA".format(period))

    @classmethod
    def VIDYA(
        cls, ohlcv: DataFrame, period: int = 9, smoothing_period: int = 12
    ) -> Series:
        """ Vidya (variable index dynamic average) indicator is a modification of the traditional Exponential Moving Average (EMA) indicator.
        The main difference between EMA and Vidya is in the way the smoothing factor F is calculated.
        In EMA the smoothing factor is a constant value F=2/(period+1);
        in Vidya the smoothing factor is variable and depends on bar-to-bar price movements."""

        raise NotImplementedError

    @classmethod
    def ER(cls, ohlc: DataFrame, period: int = 10) -> Series:
        """The Kaufman Efficiency indicator is an oscillator indicator that oscillates between +100 and -100, where zero is the center point.
         +100 is upward forex trending market and -100 is downwards trending markets."""

        change = ohlc["close"].diff(period).abs()
        volatility = ohlc["close"].diff().abs().rolling(window=period).sum()

        return pd.Series(change / volatility, name="{0} period ER".format(period))

    @classmethod
    def KAMA(
        cls,
        ohlc: DataFrame,
        er: int = 10,
        ema_fast: int = 2,
        ema_slow: int = 30,
        period: int = 20,
    ) -> Series:
        """Developed by Perry Kaufman, Kaufman's Adaptive Moving Average (KAMA) is a moving average designed to account for market noise or volatility.
        Its main advantage is that it takes into consideration not just the direction, but the market volatility as well."""

        er = cls.ER(ohlc, er)
        fast_alpha = 2 / (ema_fast + 1)
        slow_alpha = 2 / (ema_slow + 1)
        sc = pd.Series(
            (er * (fast_alpha - slow_alpha) + slow_alpha) ** 2,
            name="smoothing_constant",
        )  ## smoothing constant

        sma = pd.Series(
            ohlc["close"].rolling(period).mean(), name="SMA"
        )  ## first KAMA is SMA
        kama = []
        # Current KAMA = Prior KAMA + smoothing_constant * (Price - Prior KAMA)
        for s, ma, price in zip(
            sc.iteritems(), sma.shift().iteritems(), ohlc["close"].iteritems()
        ):
            try:
                kama.append(kama[-1] + s[1] * (price[1] - kama[-1]))
            except (IndexError, TypeError):
                if pd.notnull(ma[1]):
                    kama.append(ma[1] + s[1] * (price[1] - ma[1]))
                else:
                    kama.append(None)

        sma["KAMA"] = pd.Series(
            kama, index=sma.index, name="{0} period KAMA.".format(period)
        )  ## apply the kama list to existing index
        return sma["KAMA"]

    @classmethod
    def ZLEMA(cls, ohlc: DataFrame, period: int = 26) -> Series:
        """ZLEMA is an abbreviation of Zero Lag Exponential Moving Average. It was developed by John Ehlers and Rick Way.
        ZLEMA is a kind of Exponential moving average but its main idea is to eliminate the lag arising from the very nature of the moving averages
        and other trend following indicators. As it follows price closer, it also provides better price averaging and responds better to price swings."""

        lag = (period - 1) / 2
        return pd.Series(
            (ohlc["close"] + (ohlc["close"].diff(lag))),
            name="{0} period ZLEMA.".format(period),
        )

    @classmethod
    def WMA(cls, ohlc: DataFrame, period: int = 9, column: str = "close") -> Series:
        """
        WMA stands for weighted moving average. It helps to smooth the price curve for better trend identification.
        It places even greater importance on recent data than the EMA does.

        :period: Specifies the number of Periods used for WMA calculation
        """

        d = (period * (period + 1)) / 2  # denominator
        _weights = pd.Series(np.arange(1, period + 1))
        weights = _weights.iloc[::-1]  # reverse the series

        def linear(w):
            def _compute(x):
                return (w * x).sum() / d
            return _compute

        close_ = ohlc["close"].rolling(period, min_periods=period)
        wma = close_.apply(linear(weights))

        return pd.Series(wma, name="{0} period WMA.".format(period))

    @classmethod
    def HMA(cls, ohlc: DataFrame, period: int = 16) -> Series:
        """
        HMA indicator is a common abbreviation of Hull Moving Average.
        The average was developed by Allan Hull and is used mainly to identify the current market trend.
        Unlike SMA (simple moving average) the curve of Hull moving average is considerably smoother.
        Moreover, because its aim is to minimize the lag between HMA and price it does follow the price activity much closer.
        It is used especially for middle-term and long-term trading.
        :period: Specifies the number of Periods used for WMA calculation
        """

        import math

        half_length = int(period / 2)
        sqrt_length = int(math.sqrt(period))

        wmaf = cls.WMA(ohlc, period=half_length)
        wmas = cls.WMA(ohlc, period=period)
        ohlc['deltawma'] = 2 * wmaf - wmas
        hma = cls.WMA(ohlc, column="deltawma", period=sqrt_length)

        return pd.Series(hma, name="{0} period HMA.".format(period))

    @classmethod
    def EVWMA(cls, ohlcv: DataFrame, period: int = 20) -> Series:
        """
        The eVWMA can be looked at as an approximation to the
        average price paid per share in the last n periods.

        :period: Specifies the number of Periods used for eVWMA calculation
        """

        vol_sum = (
            ohlcv["volume"].rolling(window=period).sum()
        )  # floating shares in last N periods

        x = (vol_sum - ohlcv["volume"]) / vol_sum
        y = (ohlcv["volume"] * ohlcv["close"]) / vol_sum

        evwma = [0]

        #  evwma = (evma[-1] * (vol_sum - volume)/vol_sum) + (volume * price / vol_sum)
        for x, y in zip(x.fillna(0).iteritems(), y.iteritems()):
            if x[1] == 0 or y[1] == 0:
                evwma.append(0)
            else:
                evwma.append(evwma[-1] * x[1] + y[1])

        return pd.Series(
            Series(evwma[1:], index=ohlcv.index),
            name="{0} period EVWMA.".format(period),
        )

    @classmethod
    def VWAP(cls, ohlcv: DataFrame) -> Series:
        """
        The volume weighted average price (VWAP) is a trading benchmark used especially in pension plans.
        VWAP is calculated by adding up the dollars traded for every transaction (price multiplied by number of shares traded) and then dividing
        by the total shares traded for the day.
        """

        return pd.Series(
            ((ohlcv["volume"] * cls.TP(ohlcv)).cumsum()) / ohlcv["volume"].cumsum(),
            name="VWAP.",
        )

    @classmethod
    def SMMA(cls, ohlc: DataFrame, period: int = 42, column: str = "close") -> Series:
        """The SMMA (Smoothed Moving Average) gives recent prices an equal weighting to historic prices."""

        return pd.Series(ohlc[column].ewm(alpha=1 / period).mean(), name="SMMA")

    @classmethod
    def ALMA(
        cls, ohlc: DataFrame, period: int = 9, sigma: int = 6, offset: int = 0.85
    ) -> Series:
        """Arnaud Legoux Moving Average."""

        """dataWindow = _.last(data, period)
        size = _.size(dataWindow)
        m = offset * (size - 1)
        s = size / sigma
        sum = 0
        norm = 0
        for i in [size-1..0] by -1
        coeff = Math.exp(-1 * (i - m) * (i - m) / 2 * s * s)
        sum = sum + dataWindow[i] * coeff
        norm = norm + coeff
        return sum / norm"""

        raise NotImplementedError

    @classmethod
    def MAMA(cls, ohlc: DataFrame, period: int = 16) -> Series:
        """MESA Adaptive Moving Average"""
        raise NotImplementedError

    @classmethod
    def FRAMA(cls, ohlc: DataFrame, period: int = 16) -> Series:
        """Fractal Adaptive Moving Average"""
        raise NotImplementedError

    @classmethod
    def MACD(
        cls,
        ohlc: DataFrame,
        period_fast: int = 12,
        period_slow: int = 26,
        signal: int = 9,
    ) -> Series:
        """
        MACD, MACD Signal and MACD difference.
        The MACD Line oscillates above and below the zero line, which is also known as the centerline.
        These crossovers signal that the 12-day EMA has crossed the 26-day EMA. The direction, of course, depends on the direction of the moving average cross.
        Positive MACD indicates that the 12-day EMA is above the 26-day EMA. Positive values increase as the shorter EMA diverges further from the longer EMA.
        This means upside momentum is increasing. Negative MACD values indicates that the 12-day EMA is below the 26-day EMA.
        Negative values increase as the shorter EMA diverges further below the longer EMA. This means downside momentum is increasing.

        Signal line crossovers are the most common MACD signals. The signal line is a 9-day EMA of the MACD Line.
        As a moving average of the indicator, it trails the MACD and makes it easier to spot MACD turns.
        A bullish crossover occurs when the MACD turns up and crosses above the signal line.
        A bearish crossover occurs when the MACD turns down and crosses below the signal line.
        """

        EMA_fast = pd.Series(
            ohlc["close"]
            .ewm(ignore_na=False, span=period_fast)
            .mean(),
            name="EMA_fast",
        )
        EMA_slow = pd.Series(
            ohlc["close"]
            .ewm(ignore_na=False, span=period_slow)
            .mean(),
            name="EMA_slow",
        )
        MACD = pd.Series(EMA_fast - EMA_slow, name="MACD")
        MACD_signal = pd.Series(
            MACD.ewm(ignore_na=False, span=signal).mean(), name="SIGNAL"
        )

        return pd.concat([MACD, MACD_signal], axis=1)

    @classmethod
    def PPO(
        cls,
        ohlc: DataFrame,
        period_fast: int = 12,
        period_slow: int = 26,
        signal: int = 9,
    ) -> Series:
        """
        Percentage Price Oscillator
        PPO, PPO Signal and PPO difference.
        As with MACD, the PPO reflects the convergence and divergence of two moving averages.
        While MACD measures the absolute difference between two moving averages, PPO makes this a relative value by dividing the difference by the slower moving average
        """

        EMA_fast = pd.Series(
            ohlc["close"]
            .ewm(ignore_na=False, span=period_fast)
            .mean(),
            name="EMA_fast",
        )
        EMA_slow = pd.Series(
            ohlc["close"]
            .ewm(ignore_na=False, span=period_slow)
            .mean(),
            name="EMA_slow",
        )
        PPO = pd.Series(((EMA_fast - EMA_slow) / EMA_slow) * 100, name="PPO")
        PPO_signal = pd.Series(
            PPO.ewm(ignore_na=False, span=signal).mean(), name="SIGNAL"
        )
        PPO_histo = pd.Series(PPO - PPO_signal, name="HISTO")

        return pd.concat([PPO, PPO_signal, PPO_histo], axis=1)

    @classmethod
    def VW_MACD(
        cls,
        ohlcv: DataFrame,
        period_fast: int = 12,
        period_slow: int = 26,
        signal: int = 9,
    ) -> Series:
        """"Volume-Weighted MACD" is an indicator that shows how a volume-weighted moving average can be used to calculate moving average convergence/divergence (MACD).
        This technique was first used by Buff Dormeier, CMT, and has been written about since at least 2002."""

        vp = ohlcv["volume"] * ohlcv["close"]
        _fast = pd.Series(
            (
                vp.ewm(
                    ignore_na=False, span=period_fast
                ).mean()
            )
            / (
                ohlcv["volume"]
                .ewm(ignore_na=False, span=period_fast)
                .mean()
            ),
            name="_fast",
        )

        _slow = pd.Series(
            (
                vp.ewm(
                    ignore_na=False, span=period_slow
                ).mean()
            )
            / (
                ohlcv["volume"]
                .ewm(ignore_na=False, span=period_slow)
                .mean()
            ),
            name="_slow",
        )

        MACD = pd.Series(_fast - _slow, name="MACD")
        MACD_signal = pd.Series(
            MACD.ewm(ignore_na=False, span=signal).mean(), name="SIGNAL"
        )

        return pd.concat([MACD, MACD_signal], axis=1)

    @classmethod
    def EV_MACD(
        cls,
        ohlcv: DataFrame,
        period_fast: int = 20,
        period_slow: int = 40,
        signal: int = 9,
    ) -> Series:
        """
        Elastic Volume Weighted MACD is a variation of standard MACD,
        calculated using two EVWMA's.

        :period_slow: Specifies the number of Periods used for the slow EVWMA calculation
        :period_fast: Specifies the number of Periods used for the fast EVWMA calculation
        :signal: Specifies the number of Periods used for the signal calculation
        """

        evwma_slow = cls.EVWMA(ohlcv, period_slow)

        evwma_fast = cls.EVWMA(ohlcv, period_fast)

        MACD = pd.Series(evwma_fast - evwma_slow, name="MACD")
        MACD_signal = pd.Series(
            MACD.ewm(ignore_na=False, span=signal).mean(), name="SIGNAL"
        )

        return pd.concat([MACD, MACD_signal], axis=1)

    @classmethod
    def MOM(cls, ohlc: DataFrame, period: int = 10) -> Series:
        """Market momentum is measured by continually taking price differences for a fixed time interval.
        To construct a 10-day momentum line, simply subtract the closing price 10 days ago from the last closing price.
        This positive or negative value is then plotted around a zero line."""

        return pd.Series(ohlc["close"].diff(period), name="MOM".format(period))

    @classmethod
    def ROC(cls, ohlc: DataFrame, period: int = 12) -> Series:
        """The Rate-of-Change (ROC) indicator, which is also referred to as simply Momentum,
        is a pure momentum oscillator that measures the percent change in price from one period to the next.
        The ROC calculation compares the current price with the price “n” periods ago."""

        return pd.Series(
            (ohlc["close"].diff(period) / ohlc["close"].shift(period)) * 100, name="ROC"
        )

    @classmethod
    def RSI(cls, ohlc: DataFrame, period: int = 14) -> Series:
        """Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements.
        RSI oscillates between zero and 100. Traditionally, and according to Wilder, RSI is considered overbought when above 70 and oversold when below 30.
        Signals can also be generated by looking for divergences, failure swings and centerline crossovers.
        RSI can also be used to identify the general trend."""

        ## get the price diff
        delta = ohlc["close"].diff()

        ## positive gains (up) and negative gains (down) Series
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        # EMAs of ups and downs
        _gain = up.ewm(span=period).mean()
        _loss = down.abs().ewm(span=period).mean()

        RS = _gain / _loss
        return pd.Series(100 - (100 / (1 + RS)), name="RSI")

    @classmethod
    def IFT_RSI(
        cls, ohlc: DataFrame, rsi_period: int = 14, wma_period: int = 9
    ) -> Series:
        """Modified Inverse Fisher Transform applied on RSI.
        Suggested method to use any IFT indicator is to buy when the indicator crosses over –0.5 or crosses over +0.5
        if it has not previously crossed over –0.5 and to sell short when the indicators crosses under +0.5 or crosses under –0.5
        if it has not previously crossed under +0.5."""

        v1 = pd.Series(0.1 * (cls.RSI(ohlc, rsi_period) - 50), name="v1")

        ### v2 = WMA(wma_period) of v1
        d = (wma_period * (wma_period + 1)) / 2  # denominator
        rev = v1.iloc[::-1]  # reverse the series
        wma = []

        def _chunks(series, period):  # split into chunks of n elements
            for i in enumerate(series):
                c = rev.iloc[i[0] : i[0] + period]
                if len(c) != period:
                    yield None
                else:
                    yield c

        def _wma(chunk, period):  # calculate wma for each chunk
            w = []
            for price, i in zip(chunk.iloc[::-1].items(), range(period + 1)[1:]):
                w.append(price[1] * i / d)
            return sum(w)

        for i in _chunks(rev, wma_period):
            try:
                wma.append(_wma(i, wma_period))
            except:
                wma.append(None)

        wma.reverse()  ##reverse the wma list to match the Series

        v1["v2"] = pd.Series(wma, index=v1.index)
        fish = pd.Series(
            ((2 * v1["v2"]) - 1) ** 2 / ((2 * v1["v2"]) + 1) ** 2, name="IFT_RSI"
        )
        return fish

    @classmethod
    def SWI(cls, ohlc: DataFrame, period: int = 16) -> Series:
        """Sine Wave indicator"""
        raise NotImplementedError

    @classmethod
    def TR(cls, ohlc: DataFrame) -> Series:
        """True Range is the maximum of three price ranges.
        Most recent period's high minus the most recent period's low.
        Absolute value of the most recent period's high minus the previous close.
        Absolute value of the most recent period's low minus the previous close."""

        TR1 = pd.Series(ohlc["high"] - ohlc["low"]).abs()  # True Range = High less Low

        TR2 = pd.Series(
            ohlc["high"] - ohlc["close"].shift()
        ).abs()  # True Range = High less Previous Close

        TR3 = pd.Series(
            ohlc["close"].shift() - ohlc["low"]
        ).abs()  # True Range = Previous Close less Low

        _TR = pd.concat([TR1, TR2, TR3], axis=1)

        _TR["TR"] = _TR.max(axis=1)

        return pd.Series(_TR["TR"], name="TR")

    @classmethod
    def ATR(cls, ohlc: DataFrame, period: int = 14) -> Series:
        """Average True Range is moving average of True Range."""

        TR = cls.TR(ohlc)
        return pd.Series(
            TR.rolling(center=False, window=period).mean(),
            name="{0} period ATR".format(period),
        )

    @classmethod
    def SAR(cls, ohlc: DataFrame, af: int = 0.02, amax: int = 0.2) -> Series:
        """SAR stands for “stop and reverse,” which is the actual indicator used in the system.
        SAR trails price as the trend extends over time. The indicator is below prices when prices are rising and above prices when prices are falling.
        In this regard, the indicator stops and reverses when the price trend reverses and breaks above or below the indicator."""
        high, low = ohlc.high, ohlc.low

        # Starting values
        sig0, xpt0, af0 = True, high[0], af
        _sar = [low[0] - (high - low).std()]

        for i in range(1, len(ohlc)):
            sig1, xpt1, af1 = sig0, xpt0, af0

            lmin = min(low[i - 1], low[i])
            lmax = max(high[i - 1], high[i])

            if sig1:
                sig0 = low[i] > _sar[-1]
                xpt0 = max(lmax, xpt1)
            else:
                sig0 = high[i] >= _sar[-1]
                xpt0 = min(lmin, xpt1)

            if sig0 == sig1:
                sari = _sar[-1] + (xpt1 - _sar[-1]) * af1
                af0 = min(amax, af1 + af)

                if sig0:
                    af0 = af0 if xpt0 > xpt1 else af1
                    sari = min(sari, lmin)
                else:
                    af0 = af0 if xpt0 < xpt1 else af1
                    sari = max(sari, lmax)
            else:
                af0 = af
                sari = xpt0

            _sar.append(sari)

        return pd.Series(_sar, index=ohlc.index)

    @classmethod
    def BBANDS(
        cls, ohlc: DataFrame, period: int = 20, MA: Series = None, column: str = "close"
    ) -> Series:
        """
         Developed by John Bollinger, Bollinger Bands® are volatility bands placed above and below a moving average.
         Volatility is based on the standard deviation, which changes as volatility increases and decreases.
         The bands automatically widen when volatility increases and narrow when volatility decreases.

         This method allows input of some other form of moving average like EMA or KAMA around which BBAND will be formed.
         Pass desired moving average as <MA> argument. For example BBANDS(MA=TA.KAMA(20)).
         """

        std = ohlc["close"].rolling(window=period).std()

        if not isinstance(MA, pd.core.series.Series):
            middle_band = pd.Series(cls.SMA(ohlc, period), name="BB_MIDDLE")
        else:
            middle_band = pd.Series(MA, name="BB_MIDDLE")

        upper_bb = pd.Series(middle_band + (2 * std), name="BB_UPPER")
        lower_bb = pd.Series(middle_band - (2 * std), name="BB_LOWER")

        return pd.concat([upper_bb, middle_band, lower_bb], axis=1)

    @classmethod
    def BBWIDTH(
        cls, ohlc: DataFrame, period: int = 20, MA: Series = None, column: str = "close"
    ) -> Series:
        """Bandwidth tells how wide the Bollinger Bands are on a normalized basis."""

        BB = TA.BBANDS(ohlc, period, MA, column)

        return pd.Series(
            (BB["BB_UPPER"] - BB["BB_LOWER"]) / BB["BB_MIDDLE"],
            name="{0} period BBWITH".format(period),
        )

    @classmethod
    def PERCENT_B(
        cls, ohlc: DataFrame, period: int = 20, MA: Series = None, column: str = "close"
    ) -> Series:
        """
        %b (pronounced 'percent b') is derived from the formula for Stochastics and shows where price is in relation to the bands.
        %b equals 1 at the upper band and 0 at the lower band.
        """

        BB = TA.BBANDS(ohlc, period, MA, column)
        percent_b = pd.Series(
            (ohlc["close"] - BB["BB_LOWER"]) / (BB["BB_UPPER"] - BB["BB_LOWER"]),
            name="%b",
        )

        return percent_b

    @classmethod
    def KC(
        cls, ohlc: DataFrame, period: int = 20, atr_period: int = 10, MA: Series = None
    ) -> Series:
        """Keltner Channels [KC] are volatility-based envelopes set above and below an exponential moving average.
        This indicator is similar to Bollinger Bands, which use the standard deviation to set the bands.
        Instead of using the standard deviation, Keltner Channels use the Average True Range (ATR) to set channel distance.
        The channels are typically set two Average True Range values above and below the 20-day EMA.
        The exponential moving average dictates direction and the Average True Range sets channel width.
        Keltner Channels are a trend following indicator used to identify reversals with channel breakouts and channel direction.
        Channels can also be used to identify overbought and oversold levels when the trend is flat."""

        if not isinstance(MA, pd.core.series.Series):
            middle = pd.Series(cls.EMA(ohlc, period), name="KC_MIDDLE")
        else:
            middle = pd.Series(MA, name="KC_MIDDLE")

        up = pd.Series(middle + (2 * cls.ATR(ohlc, atr_period)), name="KC_UPPER")
        down = pd.Series(middle - (2 * cls.ATR(ohlc, atr_period)), name="KC_LOWER")

        return pd.concat([up, down], axis=1)

    @classmethod
    def DO(cls, ohlc: DataFrame, period: int = 20) -> Series:
        """Donchian Channel, a moving average indicator developed by Richard Donchian.
        It plots the highest high and lowest low over the last period time intervals."""

        upper = pd.Series(ohlc["high"].tail(period).max(), name="UPPER")
        lower = pd.Series(ohlc["low"].tail().min(), name="LOWER")
        middle = pd.Series((upper + lower) / 2, name="MIDDLE")

        return pd.concat([lower, middle, upper], axis=1)

    @classmethod
    def DMI(cls, ohlc: DataFrame, period: int = 14) -> Series:
        """The directional movement indicator (also known as the directional movement index - DMI) is a valuable tool
         for assessing price direction and strength. This indicator was created in 1978 by J. Welles Wilder, who also created the popular
         relative strength index. DMI tells you when to be long or short.
         It is especially useful for trend trading strategies because it differentiates between strong and weak trends,
         allowing the trader to enter only the strongest trends.
        source https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/dmi

        :period: Specifies the number of Periods used for DMI calculation
        """

        ohlc["up_move"] = ohlc["high"].diff()
        ohlc["down_move"] = -ohlc["low"].diff()

        DMp = []
        DMm = []

        for row in ohlc.itertuples():
            if row.up_move > row.down_move and row.up_move > 0:
                DMp.append(row.up_move)
            else:
                DMp.append(0)

            if row.down_move > row.up_move and row.down_move > 0:
                DMm.append(row.down_move)
            else:
                DMm.append(0)

        ohlc["DMp"] = DMp
        ohlc["DMm"] = DMm

        diplus = pd.Series(
            100
            * (ohlc["DMp"] / cls.ATR(ohlc, period * 6))
            .ewm(span=period)
            .mean(),
            name="DI+",
        )
        diminus = pd.Series(
            100
            * (ohlc["DMm"] / cls.ATR(ohlc, period * 6))
            .ewm(span=period)
            .mean(),
            name="DI-",
        )

        return pd.concat([diplus, diminus], axis=1)

    @classmethod
    def ADX(cls, ohlc: DataFrame, period: int = 14) -> Series:
        """The A.D.X. is 100 * smoothed moving average of absolute value (DMI +/-) divided by (DMI+ + DMI-). ADX does not indicate trend direction or momentum,
        only trend strength. Generally, A.D.X. readings below 20 indicate trend weakness,
        and readings above 40 indicate trend strength. An extremely strong trend is indicated by readings above 50"""

        dmi = cls.DMI(ohlc, period)
        return pd.Series(
            100
            * (abs(dmi["DI+"] - dmi["DI-"]) / (dmi["DI+"] + dmi["DI-"]))
            .ewm(alpha=1 / period)
            .mean(),
            name="{0} period ADX.".format(period),
        )

    @classmethod
    def PIVOT(cls, ohlc: DataFrame) -> Series:
        """
        Pivot Points are significant support and resistance levels that can be used to determine potential trades.
        The pivot points come as a technical analysis indicator calculated using a financial instrument’s high, low, and close value.
        The pivot point’s parameters are usually taken from the previous day’s trading range.
        This means you’ll have to use the previous day’s range for today’s pivot points.
        Or, last week’s range if you want to calculate weekly pivot points or, last month’s range for monthly pivot points and so on.
        """

        df = ohlc.shift()  # pivot is calculated of the previous trading session

        pivot = pd.Series(cls.TP(df), name="pivot")  # pivot is basically a lagging TP

        s1 = (pivot * 2) - df["high"]
        s2 = pivot - (df["high"] - df["low"])
        s3 = df["low"] - (2 * (df["high"] - pivot))
        s4 = df["low"] - (3 * (df["high"] - pivot))

        r1 = (pivot * 2) - df["low"]
        r2 = pivot + (df["high"] - df["low"])
        r3 = df["high"] + (2 * (pivot - df["low"]))
        r4 = df["high"] + (3 * (pivot - df["low"]))

        return pd.concat(
            [
                pivot,
                pd.Series(s1, name="s1"),
                pd.Series(s2, name="s2"),
                pd.Series(s3, name="s3"),
                pd.Series(s4, name="s4"),
                pd.Series(r1, name="r1"),
                pd.Series(r2, name="r2"),
                pd.Series(r3, name="r3"),
                pd.Series(r4, name="r4"),
            ],
            axis=1,
        )

    @classmethod
    def PIVOT_FIB(cls, ohlc: DataFrame) -> Series:
        """
        Fibonacci pivot point levels are determined by first calculating the classic pivot point,
        then multiply the previous day’s range with its corresponding Fibonacci level.
        Most traders use the 38.2%, 61.8% and 100% retracements in their calculations.
        """

        df = ohlc.shift()
        pp = pd.Series(cls.TP(df), name="pivot")  # classic pivot

        r4 = pp + ((df["high"] - df["low"]) * 1.382)
        r3 = pp + ((df["high"] - df["low"]) * 1)
        r2 = pp + ((df["high"] - df["low"]) * 0.618)
        r1 = pp + ((df["high"] - df["low"]) * 0.382)

        s1 = pp - ((df["high"] - df["low"]) * 0.382)
        s2 = pp - ((df["high"] - df["low"]) * 0.618)
        s3 = pp - ((df["high"] - df["low"]) * 1)
        s4 = pp - ((df["high"] - df["low"]) * 1.382)

        return pd.concat(
            [
                pp,
                pd.Series(s1, name="s1"),
                pd.Series(s2, name="s2"),
                pd.Series(s3, name="s3"),
                pd.Series(s4, name="s4"),
                pd.Series(r1, name="r1"),
                pd.Series(r2, name="r2"),
                pd.Series(r3, name="r3"),
                pd.Series(r4, name="r4")
            ],
            axis=1,
        )

    @classmethod
    def STOCH(cls, ohlc: DataFrame, period: int = 14) -> Series:
        """Stochastic oscillator %K
         The stochastic oscillator is a momentum indicator comparing the closing price of a security
         to the range of its prices over a certain period of time.
         The sensitivity of the oscillator to market movements is reducible by adjusting that time
         period or by taking a moving average of the result.
        """

        highest_high = ohlc["high"].rolling(center=False, window=period).max()
        lowest_low = ohlc["low"].rolling(center=False, window=period).min()

        STOCH = pd.Series(
            (ohlc["close"] - lowest_low) / (highest_high - lowest_low),
            name="{0} period STOCH %K".format(period),
        )

        return 100 * STOCH

    @classmethod
    def STOCHD(cls, ohlc: DataFrame, period: int = 3, stoch_period: int = 14) -> Series:
        """Stochastic oscillator %D
        STOCH%D is a 3 period simple moving average of %K.
        """

        return pd.Series(
            cls.STOCH(ohlc, stoch_period)
            .rolling(center=False, window=period)
            .mean(),
            name="{0} perood STOCH %D.".format(period),
        )

    @classmethod
    def STOCHRSI(
        cls, ohlc: DataFrame, rsi_period: int = 14, stoch_period: int = 14
    ) -> Series:
        """StochRSI is an oscillator that measures the level of RSI relative to its high-low range over a set time period.
        StochRSI applies the Stochastics formula to RSI values, instead of price values. This makes it an indicator of an indicator.
        The result is an oscillator that fluctuates between 0 and 1."""

        rsi = cls.RSI(ohlc, rsi_period)
        return pd.Series(
            ((rsi - rsi.min()) / (rsi.max() - rsi.min()))
            .rolling(window=stoch_period)
            .mean(),
            name="{0} period stochastic RSI.".format(rsi_period),
        )

    @classmethod
    def WILLIAMS(cls, ohlc: DataFrame, period: int = 14) -> Series:
        """Williams %R, or just %R, is a technical analysis oscillator showing the current closing price in relation to the high and low
         of the past N days (for a given N). It was developed by a publisher and promoter of trading materials, Larry Williams.
         Its purpose is to tell whether a stock or commodity market is trading near the high or the low, or somewhere in between,
         of its recent trading range.
         The oscillator is on a negative scale, from −100 (lowest) up to 0 (highest).
        """

        highest_high = ohlc["high"].rolling(center=False, window=period).max()
        lowest_low = ohlc["low"].rolling(center=False, window=period).min()

        WR = pd.Series(
            (highest_high - ohlc["close"]) / (highest_high - lowest_low),
            name="{0} Williams %R".format(period),
        )

        return WR * -100

    @classmethod
    def UO(cls, ohlc: DataFrame) -> Series:
        """Ultimate Oscillator is a momentum oscillator designed to capture momentum across three different time frames.
        The multiple time frame objective seeks to avoid the pitfalls of other oscillators.
        Many momentum oscillators surge at the beginning of a strong advance and then form bearish divergence as the advance continues.
        This is because they are stuck with one time frame. The Ultimate Oscillator attempts to correct this fault by incorporating longer
        time frames into the basic formula."""

        k = []  # current low or past close
        for row, _row in zip(ohlc.itertuples(), ohlc.shift(1).itertuples()):
            k.append(min(row.low, _row.close))
        bp = pd.Series(ohlc["close"] - k, name="bp")  # Buying pressure

        Average7 = bp.rolling(window=7).sum() / cls.TR(ohlc).rolling(window=7).sum()
        Average14 = bp.rolling(window=14).sum() / cls.TR(ohlc).rolling(window=14).sum()
        Average28 = bp.rolling(window=28).sum() / cls.TR(ohlc).rolling(window=28).sum()

        return pd.Series(
            (100 * ((4 * Average7) + (2 * Average14) + Average28)) / (4 + 2 + 1)
        )

    @classmethod
    def AO(cls, ohlc: DataFrame, slow_period: int = 34, fast_period: int = 5) -> Series:
        """'EMA', 
        Awesome Oscillator is an indicator used to measure market momentum. AO calculates the difference of a 34 Period and 5 Period Simple Moving Averages.
        The Simple Moving Averages that are used are not calculated using closing price but rather each bar's midpoints.
        AO is generally used to affirm trends or to anticipate possible reversals. """

        slow = pd.Series(
            ((ohlc["high"] + ohlc["low"]) / 2).rolling(window=slow_period).mean(),
            name="slow_AO",
        )
        fast = pd.Series(
            ((ohlc["high"] + ohlc["low"]) / 2).rolling(window=fast_period).mean(),
            name="fast_AO",
        )

        return pd.Series(fast - slow, name="AO")

    @classmethod
    def MI(cls, ohlc: DataFrame, period: int = 9) -> Series:
        """Developed by Donald Dorsey, the Mass Index uses the high-low range to identify trend reversals based on range expansions.
        In this sense, the Mass Index is a volatility indicator that does not have a directional bias.
        Instead, the Mass Index identifies range bulges that can foreshadow a reversal of the current trend."""

        _range = pd.Series(ohlc["high"] - ohlc["low"], name="range")
        EMA9 = _range.ewm(span=period, ignore_na=False).mean()
        DEMA9 = EMA9.ewm(span=period, ignore_na=False).mean()
        mass = EMA9 / DEMA9

        return pd.Series(mass.rolling(window=25).sum(), name="Mass Index").tail(period)

    @classmethod
    def VORTEX(cls, ohlc: DataFrame, period: int = 14) -> Series:
        """The Vortex indicator plots two oscillating lines, one to identify positive trend movement and the other
         to identify negative price movement.
         Indicator construction revolves around the highs and lows of the last two days or periods.
         The distance from the current high to the prior low designates positive trend movement while the
         distance between the current low and the prior high designates negative trend movement.
         Strongly positive or negative trend movements will show a longer length between the two numbers while
         weaker positive or negative trend movement will show a shorter length."""

        VMP = pd.Series(ohlc["high"] - ohlc["low"].shift(1).abs())
        VMM = pd.Series(ohlc["low"] - ohlc["high"].shift(1).abs())

        VMPx = VMP.rolling(window=period).sum()
        VMMx = VMM.rolling(window=period).sum()

        VIp = pd.Series(VMPx / cls.TR(ohlc), name="VIp").interpolate(method="index")
        VIm = pd.Series(VMMx / cls.TR(ohlc), name="VIm").interpolate(method="index")

        return pd.concat([VIm, VIp], axis=1)

    @classmethod
    def KST(
        cls, ohlc: DataFrame, r1: int = 10, r2: int = 15, r3: int = 20, r4: int = 30
    ) -> Series:
        """Know Sure Thing (KST) is a momentum oscillator based on the smoothed rate-of-change for four different time frames.
        KST measures price momentum for four different price cycles. It can be used just like any momentum oscillator.
        Chartists can look for divergences, overbought/oversold readings, signal line crossovers and centerline crossovers."""

        r1 = cls.ROC(ohlc, r1).rolling(window=10).mean()
        r2 = cls.ROC(ohlc, r2).rolling(window=10).mean()
        r3 = cls.ROC(ohlc, r3).rolling(window=10).mean()
        r4 = cls.ROC(ohlc, r4).rolling(window=15).mean()

        k = pd.Series((r1 * 1) + (r2 * 2) + (r3 * 3) + (r4 * 4), name="KST")
        signal = pd.Series(k.rolling(window=10).mean(), name="signal")

        return pd.concat([k, signal], axis=1)

    @classmethod
    def TSI(
        cls, ohlc: DataFrame, long: int = 25, short: int = 13, signal: int = 13
    ) -> Series:
        """True Strength Index (TSI) is a momentum oscillator based on a double smoothing of price changes."""

        ## Double smoother price change
        momentum = pd.Series(ohlc["close"].diff())  ## 1 period momentum
        _EMA25 = pd.Series(
            momentum.ewm(span=long, min_periods=long - 1).mean(),
            name="_price change EMA25",
        )
        _DEMA13 = pd.Series(
            _EMA25.ewm(span=short, min_periods=short - 1).mean(),
            name="_price change double smoothed DEMA13",
        )

        ## Double smoothed absolute price change
        absmomentum = pd.Series(ohlc["close"].diff().abs())
        _aEMA25 = pd.Series(
            absmomentum.ewm(span=long, min_periods=long - 1).mean(),
            name="_abs_price_change EMA25",
        )
        _aDEMA13 = pd.Series(
            _aEMA25.ewm(span=short, min_periods=short - 1).mean(),
            name="_abs_price_change double smoothed DEMA13",
        )

        TSI = pd.Series((_DEMA13 / _aDEMA13) * 100, name="TSI")
        signal = pd.Series(
            TSI.ewm(span=signal, min_periods=signal - 1).mean(), name="signal"
        )

        return pd.concat([TSI, signal], axis=1)

    @classmethod
    def TP(cls, ohlc: DataFrame) -> Series:
        """Typical Price refers to the arithmetic average of the high, low, and closing prices for a given period."""

        return pd.Series((ohlc["high"] + ohlc["low"] + ohlc["close"]) / 3, name="TP")

    @classmethod
    def ADL(cls, ohlcv: DataFrame) -> Series:
        """The accumulation/distribution line was created by Marc Chaikin to determine the flow of money into or out of a security.
        It should not be confused with the advance/decline line. While their initials might be the same, these are entirely different indicators,
        and their uses are different as well. Whereas the advance/decline line can provide insight into market movements,
        the accumulation/distribution line is of use to traders looking to measure buy/sell pressure on a security or confirm the strength of a trend."""

        MFM = pd.Series(
            (ohlcv["close"] - ohlcv["low"])
            - (ohlcv["high"] - ohlcv["close"]) / (ohlcv["high"] - ohlcv["low"]),
            name="MFM",
        )  # Money flow multiplier
        MFV = pd.Series(MFM * ohlcv["volume"], name="MFV")
        return MFV.cumsum()

    @classmethod
    def CHAIKIN(cls, ohlcv: DataFrame) -> Series:
        """Chaikin Oscillator, named after its creator, Marc Chaikin, the Chaikin oscillator is an oscillator that measures the accumulation/distribution
         line of the moving average convergence divergence (MACD). The Chaikin oscillator is calculated by subtracting a 10-day exponential moving average (EMA)
         of the accumulation/distribution line from a three-day EMA of the accumulation/distribution line, and highlights the momentum implied by the
         accumulation/distribution line."""

        return pd.Series(
            cls.ADL(ohlcv).ewm(span=3, min_periods=2).mean()
            - cls.ADL(ohlcv).ewm(span=10, min_periods=9).mean()
        )

    @classmethod
    def MFI(cls, ohlc: DataFrame, period: int = 14) -> Series:
        """The money flow index (MFI) is a momentum indicator that measures
        the inflow and outflow of money into a security over a specific period of time.
        MFI can be understood as RSI adjusted for volume.
        The money flow indicator is one of the more reliable indicators of overbought and oversold conditions, perhaps partly because
        it uses the higher readings of 80 and 20 as compared to the RSI's overbought/oversold readings of 70 and 30"""

        tp = cls.TP(ohlc)
        rmf = pd.Series(tp * ohlc["volume"], name="rmf")  ## Real Money Flow
        _mf = pd.concat([tp, rmf], axis=1)
        _mf["delta"] = _mf["TP"].diff()

        def pos(row):
            if row["delta"] > 0:
                return row["rmf"]
            else:
                return 0

        def neg(row):
            if row["delta"] < 0:
                return row["rmf"]
            else:
                return 0

        _mf["neg"] = _mf.apply(neg, axis=1)
        _mf["pos"] = _mf.apply(pos, axis=1)

        mfratio = pd.Series(
            _mf["pos"].rolling(window=period).sum()
            / _mf["neg"].rolling(window=period).sum()
        )

        return pd.Series(
            100 - (100 / (1 + mfratio)), name="{0} period MFI".format(period)
        )

    @classmethod
    def OBV(cls, ohlcv: DataFrame) -> Series:
        """
        On Balance Volume (OBV) measures buying and selling pressure as a cumulative indicator that adds volume on up days and subtracts volume on down days.
        OBV was developed by Joe Granville and introduced in his 1963 book, Granville's New Key to Stock Market Profits.
        It was one of the first indicators to measure positive and negative volume flow.
        Chartists can look for divergences between OBV and price to predict price movements or use OBV to confirm price trends."""

        obv = [0]

        for row, _row in zip(ohlcv.itertuples(), ohlcv.shift(1).itertuples()):
            if row.close > _row.close:
                obv.append(obv[-1] + row.volume)
            if row.close < _row.close:
                obv.append(obv[-1] - row.volume)
            if row.close == _row.close:
                obv.append(obv[-1])

        ohlcv["OBV"] = obv
        return pd.Series(ohlcv["OBV"], name="On Volume Balance")

    @classmethod
    def WOBV(cls, ohlcv: DataFrame) -> Series:
        """
        Weighted OBV
        Can also be seen as an OBV indicator that takes the price differences into account.
        In a regular OBV, a high volume bar can make a huge difference,
        even if the price went up only 0.01, and it it goes down 0.01
        instead, that huge volume makes the OBV go down, even though
        hardly anything really happened.
        """

        wobv = pd.Series(ohlcv["volume"] * ohlcv["close"].diff(), name="WOBV")
        return wobv.cumsum()

    @classmethod
    def VZO(cls, ohlc: DataFrame, period: int = 14) -> Series:
        """VZO uses price, previous price and moving averages to compute its oscillating value.
        It is a leading indicator that calculates buy and sell signals based on oversold / overbought conditions.
        Oscillations between the 5% and 40% levels mark a bullish trend zone, while oscillations between -40% and 5% mark a bearish trend zone.
        Meanwhile, readings above 40% signal an overbought condition, while readings above 60% signal an extremely overbought condition.
        Alternatively, readings below -40% indicate an oversold condition, which becomes extremely oversold below -60%."""

        sign = lambda a: (a > 0) - (a < 0)
        r = ohlc["close"].diff().apply(sign) * ohlc["volume"]
        dvma = r.ewm(span=period).mean()
        vma = ohlc["volume"].ewm(span=period).mean()

        return pd.Series(100 * (dvma / vma), name="VZO")

    @classmethod
    def PZO(cls, ohlc: DataFrame, period: int = 14) -> Series:
        """
        The formula for PZO depends on only one condition: if today's closing price is higher than yesterday's closing price,
        then the closing price will have a positive value (bullish); otherwise it will have a negative value (bearish).
        source: http://traders.com/Documentation/FEEDbk_docs/2011/06/Khalil.html

        :period: Specifies the number of Periods used for eVWMA calculation
        """

        sign = lambda a: (a > 0) - (a < 0)
        r = ohlc["close"].diff().apply(sign) * ohlc["close"]
        cp = pd.Series(r.ewm(span=period).mean())
        tc = cls.EMA(ohlc, period)

        return pd.Series(100 * (cp / tc), name="{} period PZO".format(period))

    @classmethod
    def EFI(cls, ohlcv: DataFrame, period: int = 13) -> Series:
        """Elder's Force Index is an indicator that uses price and volume to assess the power
         behind a move or identify possible turning points."""

        fi = pd.Series((ohlcv["close"] - ohlcv["close"].diff()) * ohlcv["volume"])
        return pd.Series(
            fi.ewm(ignore_na=False, span=period).mean(),
            name="{0} period Force Index".format(period),
        )

    @classmethod
    def CFI(cls, ohlcv: DataFrame) -> Series:
        """
        Cummulative Force Index.
        Adopted from  Elder's Force Index.
        """

        fi1 = pd.Series(ohlcv["volume"] * ohlcv["close"].diff())
        cfi = pd.Series(
            fi1.ewm(ignore_na=False, min_periods=9, span=10).mean(), name="CFI"
        )

        return cfi.cumsum()

    @classmethod
    def EBBP(cls, ohlc: DataFrame) -> Series:
        """Bull power and bear power by Dr. Alexander Elder show where today’s high and low lie relative to the a 13-day EMA"""

        bull_power = pd.Series(ohlc["high"] - cls.EMA(ohlc, 13), name="Bull.")
        bear_power = pd.Series(ohlc["low"] - cls.EMA(ohlc, 13), name="Bear.")

        return pd.concat([bull_power, bear_power], axis=1)

    @classmethod
    def EMV(cls, ohlcv: Series, period: int = 14) -> Series:
        """Ease of Movement (EMV) is a volume-based oscillator that fluctuates above and below the zero line.
        As its name implies, it is designed to measure the 'ease' of price movement.
        prices are advancing with relative ease when the oscillator is in positive territory.
        Conversely, prices are declining with relative ease when the oscillator is in negative territory."""

        distance = pd.Series(
            ((ohlcv["high"] + ohlcv["low"]) / 2)
            - (ohlcv["high"].diff() - ohlcv["low"].diff()) / 2
        )
        box_ratio = pd.Series(
            (ohlcv["volume"] / 1000000) / (ohlcv["high"] - ohlcv["low"])
        )

        _emv = pd.Series(distance / box_ratio)

        return pd.Series(
            _emv.rolling(window=period).mean(), name="{0} period EMV.".format(period)
        )

    @classmethod
    def CCI(cls, ohlc: DataFrame, period: int = 20) -> Series:
        """Commodity Channel Index (CCI) is a versatile indicator that can be used to identify a new trend or warn of extreme conditions.
        CCI measures the current price level relative to an average price level over a given period of time.
        The CCI typically oscillates above and below a zero line. Normal oscillations will occur within the range of +100 and −100.
        Readings above +100 imply an overbought condition, while readings below −100 imply an oversold condition.
        As with other overbought/oversold indicators, this means that there is a large probability that the price will correct to more representative levels."""

        tp = cls.TP(ohlc)
        return pd.Series(
            (tp - tp.rolling(window=period).mean()) / (0.015 * tp.mad()),
            name="{0} period CCI".format(period),
        )

    @classmethod
    def COPP(cls, ohlc: DataFrame) -> Series:
        """The Coppock Curve is a momentum indicator, it signals buying opportunities when the indicator moved from negative territory to positive territory."""

        roc1 = cls.ROC(ohlc, 14)
        roc2 = cls.ROC(ohlc, 11)

        return pd.Series(
            (roc1 + roc2).ewm(span=10, min_periods=9).mean(), name="Coppock Curve"
        )

    @classmethod
    def BASP(cls, ohlc: DataFrame, period: int = 40) -> Series:
        """BASP indicator serves to identify buying and selling pressure."""

        sp = ohlc["high"] - ohlc["close"]
        bp = ohlc["close"] - ohlc["low"]
        spavg = sp.ewm(span=period).mean()
        bpavg = bp.ewm(span=period).mean()

        nbp = bp / bpavg
        nsp = sp / spavg

        varg = ohlc["volume"].ewm(span=period).mean()
        nv = ohlc["volume"] / varg

        nbfraw = pd.Series(nbp * nv, name="Buy.")
        nsfraw = pd.Series(nsp * nv, name="Sell.")

        return pd.concat([nbfraw, nsfraw], axis=1)

    @classmethod
    def BASPN(cls, ohlc: DataFrame, period: int = 40) -> Series:
        """
        Normalized BASP indicator
        """

        sp = ohlc["high"] - ohlc["close"]
        bp = ohlc["close"] - ohlc["low"]
        spavg = sp.ewm(span=period).mean()
        bpavg = bp.ewm(span=period).mean()

        nbp = bp / bpavg
        nsp = sp / spavg

        varg = ohlc["volume"].ewm(span=period).mean()
        nv = ohlc["volume"] / varg

        nbf = pd.Series((nbp * nv).ewm(span=20).mean(), name="Buy.")
        nsf = pd.Series((nsp * nv).ewm(span=20).mean(), name="Sell.")

        return pd.concat([nbf, nsf], axis=1)

    @classmethod
    def CMO(cls, ohlc: DataFrame, period: int = 9) -> DataFrame:
        """
        Chande Momentum Oscillator (CMO) - technical momentum indicator invented by the technical analyst Tushar Chande.
        It is created by calculating the difference between the sum of all recent gains and the sum of all recent losses and then
        dividing the result by the sum of all price movement over the period.
        This oscillator is similar to other momentum indicators such as the Relative Strength Index and the Stochastic Oscillator
        because it is range bounded (+100 and -100)."""

        mom = ohlc["close"].diff().abs()
        sma_mom = mom.rolling(window=period).mean()
        mom_len = ohlc["close"].diff(period)

        return pd.Series(100 * (mom_len / (sma_mom * period)))

    @classmethod
    def CHANDELIER(
        cls, ohlc: DataFrame, period_1: int = 14, period_2: int = 22, k: int = 3
    ) -> Series:
        """
        Chandelier Exit sets a trailing stop-loss based on the Average True Range (ATR).

        The indicator is designed to keep traders in a trend and prevent an early exit as long as the trend extends.

        Typically, the Chandelier Exit will be above prices during a downtrend and below prices during an uptrend.
        """

        l = pd.Series(
            ohlc["close"].rolling(window=period_2).max() - cls.ATR(ohlc, 22) * k,
            name="Long.",
        )
        s = pd.Series(
            ohlc["close"].rolling(window=period_1).min() - cls.ATR(ohlc, 22) * k,
            name="Short.",
        )

        return pd.concat([s, l], axis=1)

    @classmethod
    def QSTICK(cls, ohlc: DataFrame, period: int = 14) -> Series:
        """
        QStick indicator shows the dominance of black (down) or white (up) candlesticks, which are red and green in Chart,
        as represented by the average open to close change for each of past N days."""

        _close = ohlc["close"].tail(period)
        _open = ohlc["open"].tail(period)

        return pd.Series(
            (_close - _open) / period, name="{0} period QSTICK.".format(period)
        )

    @classmethod
    def TMF(cls, ohlcv: DataFrame, period: int = 21) -> Series:
        """Indicator by Colin Twiggs which improves upon CMF.
        source: https://user42.tuxfamily.org/chart/manual/Twiggs-Money-Flow.html"""

        ohlcv["ll"] = [min(l, c) for l, c in zip(ohlcv["low"], ohlcv["close"].shift(1))]
        ohlcv["hh"] = [
            max(h, c) for h, c in zip(ohlcv["high"], ohlcv["close"].shift(1))
        ]

        ohlcv["range"] = (
            2 * ((ohlcv["close"] - ohlcv["ll"]) / (ohlcv["hh"] - ohlcv["ll"])) - 1
        )
        ohlcv["rangev"] = None

        # TMF Signal Line = EMA(TMF)
        # return TMF
        raise NotImplementedError

    @classmethod
    def WTO(
        cls, ohlc: DataFrame, channel_lenght: int = 10, average_lenght: int = 21
    ) -> Series:
        """
        Wave Trend Oscillator
        source: http://www.fxcoaching.com/WaveTrend/
        """

        ap = cls.TP(ohlc)
        esa = ap.ewm(span=channel_lenght).mean()
        d = pd.Series((ap - esa).abs().ewm(span=channel_lenght).mean(), name="d")
        ci = (ap - esa) / (0.015 * d)

        wt1 = pd.Series(ci.ewm(span=average_lenght).mean(), name="WT1.")
        wt2 = pd.Series(wt1.rolling(window=4).mean(), name="WT2.")

        return pd.concat([wt1, wt2], axis=1)

    @classmethod
    def FISH(cls, ohlc: DataFrame, period: int = 10) -> Series:
        """
        Fisher Transform was presented by John Ehlers. It assumes that price distributions behave like square waves.

        The Fisher Transform uses the mid-point or median price in a series of calculations to produce an oscillator.

        A signal line which is a previous value of itself is also calculated.
        """

        from numpy import log

        med = (ohlc["high"] + ohlc["low"]) / 2
        ndaylow = med.rolling(window=period).min()
        ndayhigh = med.rolling(window=period).max()
        raw = (2 * ((med - ndaylow) / (ndayhigh - ndaylow))) - 1
        smooth = raw.ewm(span=5).mean()
        _smooth = smooth.fillna(0)

        return pd.Series(
            (log((1 + _smooth) / (1 - _smooth))).ewm(span=3).mean(),
            name="{0} period FISH.".format(period),
        )

    @classmethod
    def ICHIMOKU(cls, ohlc: DataFrame) -> Series:
        """
        The Ichimoku Cloud, also known as Ichimoku Kinko Hyo, is a versatile indicator that defines support and resistance,
        identifies trend direction, gauges momentum and provides trading signals.

        Ichimoku Kinko Hyo translates into “one look equilibrium chart”.
        """

        tenkan_sen = pd.Series(
            (
                ohlc["high"].rolling(window=9).mean()
                + ohlc["low"].rolling(window=9).mean()
            )
            / 2,
            name="TENKAN",
        )  ## conversion line
        kijun_sen = pd.Series(
            (
                ohlc["high"].rolling(window=26).mean()
                + ohlc["low"].rolling(window=26).mean()
            )
            / 2,
            name="KIJUN",
        )  ## base line

        senkou_span_a = pd.Series(
            ((tenkan_sen + kijun_sen) / 2), name="senkou_span_a"
        )  ## Leading span
        senkou_span_b = pd.Series(
            (
                (
                    ohlc["high"].rolling(window=52).mean()
                    + ohlc["low"].rolling(window=52).mean()
                )
                / 2
            ),
            name="SENKOU",
        )
        chikou_span = pd.Series(
            ohlc["close"].shift(-26).rolling(window=26).mean(), name="CHIKOU"
        )

        return pd.concat(
            [tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b, chikou_span], axis=1
        )

    @classmethod
    def APZ(
        cls, ohlc: DataFrame, period: int = 21, dev_factor: int = 2, MA: Series = None
    ) -> Series:
        """
        The adaptive price zone (APZ) is a technical indicator developed by Lee Leibfarth.

        The APZ is a volatility based indicator that appears as a set of bands placed over a price chart.

        Especially useful in non-trending, choppy markets,

        the APZ was created to help traders find potential turning points in the markets.
        """

        if not isinstance(MA, pd.Series):
            MA = cls.DEMA(ohlc, period)
        price_range = pd.Series(
            (ohlc["high"] - ohlc["low"]).ewm(span=period).mean()
        )
        volatility_value = pd.Series(
            price_range.ewm(span=period).mean(), name="vol_val"
        )

        # upper_band = dev_factor * volatility_value + dema
        upper_band = pd.Series((volatility_value * dev_factor) + MA, name="UPPER")
        lower_band = pd.Series(MA - (volatility_value * dev_factor), name="LOWER")

        return pd.concat([upper_band, lower_band], axis=1)

    @classmethod
    def VR(cls, ohlc: DataFrame, period: int = 14) -> Series:
        """
        Vector Size Indicator
        :param pd.DataFrame ohlc: 'open, high, low, close' pandas DataFrame
        :return pd.Series: indicator calcs as pandas Series
        """

        import numpy as np

        vector_size = len(ohlc.close)
        high_low_diff = ohlc.high - ohlc.low
        high_close_diff = np.zeros(vector_size)
        high_close_diff[1:] = np.abs(ohlc.high[1:] - ohlc.close[0 : vector_size - 1])
        low_close_diff = np.zeros(vector_size)
        low_close_diff[1:] = np.abs(ohlc.low[1:] - ohlc.close[0 : vector_size - 1])
        vectors_stacked = np.vstack((high_low_diff, high_close_diff, low_close_diff))

        tr = np.amax(vectors_stacked, axis=0)
        vr = pd.Series(
            tr / cls.EMA(ohlc.close, period=periods),
            name="{0} period VR.".format(period),
        )

        return vr

    @classmethod
    def SQZMI(cls, ohlc: DataFrame, period: int = 20, MA: Series = None) -> Series:
        """
        Squeeze Momentum Indicator

        The Squeeze indicator attempts to identify periods of consolidation in a market.
        In general the market is either in a period of quiet consolidation or vertical price discovery.
        By identifying these calm periods, we have a better opportunity of getting into trades with the potential for larger moves.
        Once a market enters into a “squeeze”, we watch the overall market momentum to help forecast the market direction and await a release of market energy.

        :param pd.DataFrame ohlc: 'open, high, low, close' pandas DataFrame
        :period: int - number of periods to take into consideration
        :MA pd.Series: override internal calculation which uses SMA with moving average of your choice
        :return pd.Series: indicator calcs as pandas Series

        SQZMI['SQZ'] is bool True/False, if True squeeze is on. If false, squeeeze has fired.
        """

        if not isinstance(MA, pd.core.series.Series):
            ma = pd.Series(cls.SMA(ohlc, period))
        else:
            ma = None

        bb = cls.BBANDS(ohlc, period=period, MA=ma)
        kc = cls.KC(ohlc, period=period)
        comb = pd.concat([bb, kc], axis=1)

        def sqz_on(row):
            if row["BB_LOWER"] > row["KC_LOWER"] and row["BB_UPPER"] < row["KC_UPPER"]:
                return True
            else:
                return False

        comb["SQZ"] = comb.apply(sqz_on, axis=1)

        return pd.Series(comb["SQZ"], name="{0} period SQZMI".format(period))

    @classmethod
    def VPT(cls, ohlc: DataFrame) -> Series:
        """
        Volume Price Trend
        The Volume Price Trend uses the difference of price and previous price with volume and feedback to arrive at its final form.
        If there appears to be a bullish divergence of price and the VPT (upward slope of the VPT and downward slope of the price) a buy opportunity exists.
        Conversely, a bearish divergence (downward slope of the VPT and upward slope of the price) implies a sell opportunity.
        """

        hilow = (ohlc["high"] - ohlc["low"]) * 100
        openclose = (ohlc["close"] - ohlc["open"]) * 100
        vol = ohlc["volume"] / hilow
        spreadvol = (openclose * vol).cumsum()

        vpt = spreadvol + spreadvol

        return pd.Series(vpt, name="VPT")

    @classmethod
    def FVE(cls, ohlc: DataFrame, period: int = 22, factor: int = 0.3) -> Series:
        """
        FVE is a money flow indicator, but it has two important innovations: first, the F VE takes into account both intra and
        interday price action, and second, minimal price changes are taken into account by introducing a price threshold.
        """

        hl2 = (ohlc["high"] + ohlc["low"]) / 2
        tp = TA.TP(ohlc)
        smav = ohlc["volume"].rolling(window=period).mean()
        mf = pd.Series((ohlc["close"] - hl2 + tp.diff()), name="mf")

        _mf = pd.concat([ohlc["close"], ohlc["volume"], mf], axis=1)

        def vol_shift(row):

            if row["mf"] > factor * row["close"] / 100:
                return row["volume"]
            elif row["mf"] < -factor * row["close"] / 100:
                return -row["volume"]
            else:
                return 0

        _mf["vol_shift"] = _mf.apply(vol_shift, axis=1)
        _sum = _mf["vol_shift"].rolling(window=period).sum()

        return pd.Series((_sum / smav) / period * 100)

    @classmethod
    def VFI(
        cls,
        ohlc: DataFrame,
        period: int = 130,
        smoothing_factor: int = 3,
        factor: int = 0.2,
        vfactor: int = 2.5,
    ) -> Series:
        """
        This indicator tracks volume based on the direction of price
        movement. It is similar to the On Balance Volume Indicator.
        For more information see "Using Money Flow to Stay with the Trend",
        and "Volume Flow Indicator Performance" in the June 2004 and
        July 2004 editions of Technical Analysis of Stocks and Commodities.

        :period: Specifies the number of Periods used for VFI calculation
        :factor: Specifies the fixed scaling factor for the VFI calculation
        :vfactor: Specifies the cutoff for maximum volume in the VFI calculation
        :smoothing_factor: Specifies the number of periods used in the short moving average
        """

        import numpy as np

        typical = TA.TP(ohlc)
        # historical interday volatility and cutoff
        inter = typical.apply(np.log).diff()
        # stdev of linear1
        vinter = inter.rolling(window=30).std()
        cutoff = pd.Series(factor * vinter * ohlc["close"], name="cutoff")
        price_change = pd.Series(typical.diff(), name="pc")  # price change
        mav = pd.Series(
            ohlc["volume"]
            .rolling(center=False, window=period)
            .mean(),
            name="mav",
        )

        _va = pd.concat([ohlc["volume"], mav.shift()], axis=1)
        _mp = pd.concat([price_change, cutoff], axis=1)
        _mp.fillna(value=0, inplace=True)

        def _vol_added(row):
            """ Determine the maximum volume to be added"""

            if row["volume"] > vfactor * row["mav"]:
                return vfactor * row["mav"]
            else:
                return row["volume"]

        added_vol = _va.apply(_vol_added, axis=1)

        def _multiplier(row):
            """
            Determine whether the volume is up volume (multiplier +1) or
            down volume (multiplier -1). If price change is smaller than cutoff
            do not count volume (multipler 0).
            """
            if row["pc"] > row["cutoff"]:
                return 1
            elif row["pc"] < 0 - row["cutoff"]:
                return -1
            else:
                return 0

        multiplier = _mp.apply(_multiplier, axis=1)
        raw_sum = (multiplier * added_vol).rolling(window=period).sum()
        raw_value = raw_sum / mav.shift()

        vfi = pd.Series(
            raw_value.ewm(
                ignore_na=False, min_periods=smoothing_factor - 1, span=smoothing_factor
            ).mean(),
            name="VFI",
        )

        return vfi

    @classmethod
    def MSD(cls, ohlc: DataFrame, period: int = 21, ddof: int = 1) -> Series:
        """
        Standard deviation is a statistical term that measures the amount of variability or dispersion around an average.
        Standard deviation is also a measure of volatility. Generally speaking, dispersion is the difference between the actual value and the average value.
        The larger this dispersion or variability is, the higher the standard deviation.
        Standard Deviation values rise significantly when the analyzed contract of indicator change in value dramatically.
        When markets are stable, low Standard Deviation readings are normal.
        Low Standard Deviation readings typically tend to come before significant upward changes in price.
        Analysts generally agree that high volatility is part of major tops, while low volatility accompanies major bottoms.

        :period: Specifies the number of Periods used for MSD calculation
        :ddof: Delta Degrees of Freedom. The divisor used in calculations is N - ddof, where N represents the number of elements.
        """

        return pd.Series(ohlc["close"].rolling(period).std(), name="MSD")


if __name__ == "__main__":
    print([k for k in TA.__dict__.keys() if k[0] not in "_"])
