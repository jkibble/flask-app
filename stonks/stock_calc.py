import requests
import pandas as pd
import numpy as np
import yfinance as yf

from stonks.alpaca_client import getAlpacaStocks
from stonks.yahoo_client import getYahooStocks
from stonks.yfinance_client import getYFinanceStocks

class Stonks:
    def tickerSearch(self, search):
        response = requests.get(
            f'http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={search}&region=1&lang=en'
        )
        results = response.json()

        return results['ResultSet']['Result']

    def getCompanyInfo(self, ticker):
        company = yf.Ticker(ticker)
        return company.info

    def calculateEWMCrossover(self, df, short, long):
        df['short']  = df['close'].ewm(span=int(short), adjust=False).mean()
        df['long']   = df['close'].ewm(span=int(long), adjust=False).mean()
        return df

    def calculateSMACrossover(self, df, short, long):
        df['short']  = df['close'].rolling(window=int(short), min_periods=1).mean()
        df['long']   = df['close'].rolling(window=int(long), min_periods=1).mean()
        return df

    def calculateCrossover(self, df, short, long, movingAverage):
        if movingAverage == 'SMA':
            df = self.calculateSMACrossover(df, short, long)
        else:
            df = self.calculateEWMCrossover(df, short, long)

        df['change'] = df['close'].pct_change() * 100

        df['signal'] = np.where(df['short'] < df['long'], 1.0, 0.0)
        df['position'] = df['signal'].diff()
        df['buy'] = np.where(df['position'] == 1.0, df['close'], float("nan"))
        df['sell'] = np.where(
            (df['position'] == -1.0) | (df['change'] < -15),
            df['close'],
            float("nan")
        )

        return df

    def getStonks(self, tickers, short=5, long=20, timeframe='1D', movingAverage='SMA'):
        symbols = tickers.upper().strip().split(' ')

        df = getYFinanceStocks(symbols=symbols, timeframe=timeframe, limit=30)

        return df.groupby('symbol').apply(self.calculateCrossover, short=short, long=long, movingAverage=movingAverage)
