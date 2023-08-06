"""
    Functions to create data series for some technical indicators,
    which could be charted using various charting tools

        SMA  - Simple moving average
        EMA  - Exponential moving average
        MACD - Moving average convergence divergence
        OBV  - On balance volume
        SSO  - Slow stochastic Oscillator
"""

import datetime
import pandas as pd
import yfinance as yf

from pandas_datareader import data as pdr

# Column names from yfinance
COLUMN_VOLUME="Volume"
COLUMN_CLOSE="Adj Close"
COLUMN_HIGH="High"
COLUMN_LOW="Low"

# On balance volume
OBV_LABEL="OnBalanceVolume"
DEFAULT_OBV_DAYS=60

# MACD Labels
MACD_LABEL="MACD"
MACD_DIVERGENCE="Divergence"
MACD_SIGNAL_LINE="SignalLine"
DEFAULT_MACD_LONG_PERIOD=26
DEFAULT_MACD_SHORT_PERIOD=12
DEFAULT_MACD_SIGNAL=9

# Slow Stochastics Labels
SS_PERIOD_HIGH="PeriodHigh"
SS_PERIOD_LOW="PeriodLow"
SS_FAST_K="FastK"
SS_K="%K"
SS_D="%D"
DEFAULT_SS_PERIOD=14
DEFAULT_SS_K=3
DEFAULT_SS_D=3

DEFAULT_DAYS=365
DAY_IN_SECONDS=24 * 60 * 60

def get_historical_data(symbol,days=DEFAULT_DAYS):
    """ Get historical stock data using the yfinance module

        symbol -> ticker symbol
        days   -> number of *calendar* days of data to fetch

        The end date is the current date.

        Example:
            stock_data = get_historical_data(symbol)
            quarter_data = get_historical_data(symbol,90)
    """
    end_date = datetime.datetime.now()
    start_date = datetime.datetime.fromtimestamp(end_date.timestamp() - (days * DAY_IN_SECONDS))
    return get_historical_data_range(symbol,start_date,end_date)

def get_historical_data_range(symbol,start_date,end_date):
    """ Get historical stock data using the yfinance module

        symbol     -> ticker symbol
        start_date -> python datetime object for the start of the series
        end_date   -> python datetime object for the end of the series

        Example:
            stock_data = get_historical_data_range(symbol,start_date,end_date)
    """
    yf.pdr_override()
    return pdr.get_data_yahoo(symbol,start=start_date,end=end_date)

def SMA(data_series,periods):
    """ Calculate the simple moving average 

        data_series -> pandas Series
        periods     -> the number of periods used to calculate

        Example:
            stock_data = get_historical_data(symbol)
            three_day_sma = SMA(stock_data['Volume'],3)
    """
    return data_series.rolling(window=periods).mean()

def EMA(data_series,periods):
    """ Calculate the exponential moving average 

        data_series -> pandas Series
        periods     -> the number of periods used to calculate

        Example:
            stock_data = get_historical_data(symbol)
            three_day_ema = EMA(stock_data['Close'],3)
    """
    return data_series.ewm(span=periods,adjust=False).mean()

def MACD(data_series,
        long_period=DEFAULT_MACD_LONG_PERIOD,
        short_period=DEFAULT_MACD_SHORT_PERIOD,
        signal=DEFAULT_MACD_SIGNAL):
    """ Calculates the MACD (Moving Average Convergence Divergence)

        long_period  -> the number of periods for the long window
        short_period -> the number of periods for the short window
        signal       -> the number of periods to use for the signal line

        Example:
            stock_data = get_historical_data(symbol)
            macd = MACD(stock_data['Adj Close'])
    """
    macd = pd.DataFrame(data_series)

    shortEMA = EMA(data_series,short_period)
    longEMA = EMA(data_series,long_period)

    macd[MACD_LABEL] = shortEMA - longEMA
    macd[MACD_SIGNAL_LINE] = EMA(macd[MACD_LABEL],signal)
    macd[MACD_DIVERGENCE] = macd[MACD_LABEL] - macd[MACD_SIGNAL_LINE]

    return macd

def OBV(close_series,volume_series,days=DEFAULT_OBV_DAYS):
    """ Calculates the On Balance Volume

        close_series  -> pandas Series with the closing price data
        volume_series -> pandas Series with the volume data
        days          -> number of days to use to calculate

        Example:
            stock_data = get_historical_data(symbol)
            obv_data = OBV(stock_data['Adj Close'],stock_data['Volume'])
    """
    day_index = -1 * days
    volume_data = pd.DataFrame(volume_series)[day_index:]
    volume_data[COLUMN_CLOSE] = pd.DataFrame(close_series)[day_index:]

    for i, (index, row) in enumerate(volume_data.iterrows()):
        if i > 0:
            # Not the first row, so adjust OBV based on the price action
            prev_obv = volume_data.loc[volume_data.index[i - 1], OBV_LABEL]
            if row[COLUMN_CLOSE] > volume_data.loc[volume_data.index[i - 1], COLUMN_CLOSE]:
                # Up day
                obv = prev_obv + row[COLUMN_VOLUME]
            elif row[COLUMN_CLOSE] < volume_data.loc[volume_data.index[i - 1], COLUMN_CLOSE]:
                # Down day
                obv = prev_obv - row[COLUMN_VOLUME]
            else:
                # Equals, so keep the previous OBV value
                obv = prev_obv
        else:
            # First row, set prev_obv to zero
            obv = row[COLUMN_VOLUME]
            prev_obv = 0

        # Assign the obv value to the correct row
        volume_data.at[index, OBV_LABEL] = obv

    return volume_data

def SSO(close_series,high_series,low_series,
        period=DEFAULT_SS_PERIOD,
        k=DEFAULT_SS_K,
        d=DEFAULT_SS_D):
    """ Calculates the Slow Stochastic Oscillator

        period -> the number of periods for fast %K 
        k      -> the number of periods for %K
        d      -> the number of periods for %D

        Example:
            stock_data = get_historical_data(symbol)
            slow_stochastics = SSO(stock_data['Close'])
    """
    # Start with the close prices
    ss = pd.DataFrame(close_series)

    # Grab the highest high and lowest low for the period
    ss[SS_PERIOD_LOW] = low_series.rolling(window=period).min()
    ss[SS_PERIOD_HIGH] = high_series.rolling(window=period).max()

    # Calculate the fast %K value
    ss[SS_FAST_K] = 100*((close_series - ss[SS_PERIOD_LOW]) / (ss[SS_PERIOD_HIGH] - ss[SS_PERIOD_LOW]) )

    # Slow %K is the SMA of the fast %k
    ss[SS_K] = SMA(ss[SS_FAST_K],k)

    # %D is the SMA of the Slow %K
    ss[SS_D] = SMA(ss[SS_K],d)

    return ss

