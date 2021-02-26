from datetime import datetime, timedelta
import numpy as np

import pandas as pd
import pandas_datareader.data as web
import requests
import yfinance as yf

class stonks:
  def tickerSearch(ticker):
    response = requests.get(f'https://financialmodelingprep.com/api/v3/search?query={ticker}&limit=5&apikey=demo')
    return response.json()

  def getCompanyInfo(ticker):
    company = yf.Ticker(ticker)
    return company.info

  def getStonks(ticker):

    start = datetime.today() - timedelta(days = 365)
    end = datetime.today()

    stocks = web.DataReader(ticker, 'yahoo', start = start, end = end)
    stocks['previous7daylow'] = stocks['Low'].rolling(window = 7).min()
    stocks['previous7dayhigh'] = stocks['Low'].rolling(window = 7).max()
    stocks['previous200dayclose'] = stocks['Close'].ewm(span = 200, adjust = False).mean()
    stocks['buy'] = np.where(stocks['previous7daylow'] > stocks['previous200dayclose'], 1.0, 0.0)
    stocks['sell'] = np.where(stocks['Close'] > stocks['previous7dayhigh'], 1.0, 0.0)
    stocks['Datetime'] = stocks.index.map(str)

    return stocks.tail(30).to_dict('list')
