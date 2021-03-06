import requests
import pandas as pd
import numpy as np
import yfinance as yf

from datetime import datetime, timedelta
from stonks.yahoo_client import YahooClient
from stonks.yfinance_client import YfinanceClient

class Stonks:
    def __init__(self):
        # self.client = YahooClient()
        self.client = YfinanceClient()

    def tickerSearch(self, search):
        response = requests.get(
            f'http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={search}&region=1&lang=en'
        )
        results = response.json()

        return results['ResultSet']['Result']

    def getCompanyInfo(self, ticker):
        company = yf.Ticker(ticker)
        return company.info

    def calculateEWMPosition(self, df, short, long):
        print('calculating EWM')
        df['short']  = df['close'].ewm(span=int(short), adjust=False).mean()
        df['long']   = df['close'].ewm(span=int(long), adjust=False).mean()
        df['signal'] = np.where(df['short'] < df['long'], 1.0, 0.0)
        df['position'] = df['signal'].diff()

        return df

    def calculateSMAPosition(self, df, short, long):
        print('calculating SMA')
        df['short']  = df['close'].rolling(window=int(short), min_periods=1).mean()
        df['long']   = df['close'].rolling(window=int(long), min_periods=1).mean()
        df['signal'] = np.where(df['short'] < df['long'], 1.0, 0.0)
        df['position'] = df['signal'].diff()

        return df

    def calculateRSIPosition(self, df, short, long):
        print('calculating RSI')
        delta = df['close'].diff(1)
        delta.dropna(inplace=True)

        positive = delta.copy()
        negative = delta.copy()

        positive[positive < 0] = 0
        negative[negative > 0] = 0

        average_gain = positive.rolling(window=int(long), min_periods=2).mean()
        average_loss = abs(negative.rolling(window=int(long), min_periods=2).mean())
        relative_strength = average_gain / average_loss

        df['RSI'] = 100.0 - (100.0 / (1.0 + relative_strength))
        df['signal'] = 0.0
        df.loc[df['RSI'] > 70, 'signal'] = -1.0
        df.loc[df['RSI'] < 30, 'signal'] = 1.0
        df['position'] = df['signal'].diff()

        return df


    def calculateCrossover(self, df, short, long, movingAverage):
        if movingAverage == 'SMA':
            df = self.calculateSMAPosition(df, short, long)
        elif movingAverage == 'EWM':
            df = self.calculateEWMPosition(df, short, long)
        elif movingAverage == 'RSI':
            df = self.calculateRSIPosition(df, short, long)

        df['change'] = df['close'].pct_change() * 100
        df['buy'] = np.where(df['position'] == 1.0, df['close'], float("nan"))
        df['sell'] = np.where(df['position'] == -1.0, df['close'], float("nan"))

        return df

    def getStonks(self, tickers, short=5, long=20, timeframe='1D', movingAverage='SMA'):
        symbols = tickers.upper().strip().split(' ')
        df = self.client.getStocks(symbols, timeframe, 30)
        calculated = df.groupby('symbol').apply(self.calculateCrossover, short=short, long=long, movingAverage=movingAverage)

        yesterday = (datetime.today() - timedelta(days=1))
        today     = datetime.today()

        print(yesterday, today)

        return calculated.sort_index().loc[yesterday:today]
