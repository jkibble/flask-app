from datetime import datetime, timedelta
import numpy as np

import pandas as pd
import pandas_datareader.data as web
import requests
import yfinance as yf


class stonks:
    def tickerSearch(search):
        response = requests.get(
            f'http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={search}&region=1&lang=en'
        )
        results = response.json()

        return results['ResultSet']['Result']

    def getCompanyInfo(ticker):
        company = yf.Ticker(ticker)
        return company.info

    def getStonks(ticker, short = 5, long = 10, days = 60, money = 1000):

        start = datetime.today() - timedelta(days = int(days))
        end = datetime.today()

        df = web.DataReader(ticker, 'yahoo', start = start, end = end)

        df['Short'] = df['Close'].rolling(window = int(short), min_periods = 1).mean()
        df['Long'] = df['Close'].rolling(window = int(long), min_periods = 1).mean()

        df['Drop'] = df['Close'].pct_change() * 100
        df['Signal'] = np.where(df['Short'] > df['Long'], 1.0, 0.0)
        df['Position'] = df['Signal'].diff()
        df['Buy'] = np.where(df['Position'] == 1.0, df['Close'], float("nan"))
        df['Sell'] = np.where(
          (df['Position'] == -1.0) | (df['Drop'] < -20),
          df['Close'],
          float("nan")
        )
        df['Datetime'] = df.index.strftime('%Y-%m-%d')

        df.drop(['High', 'Low', 'Open', 'Volume', 'Adj Close'], axis = 1, inplace = True)

        return df
