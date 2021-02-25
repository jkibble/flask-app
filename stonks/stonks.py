from datetime import datetime, timedelta

import pandas as pd
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
    company = yf.Ticker(ticker)
    stocks = company.history(period='5d', interval='60m')
    stocks['Open_EMA'] = stocks['Open'].ewm(span = 50, adjust = False).mean()
    stocks['Close_EMA'] = stocks['Close'].ewm(span = 50, adjust = False).mean()
    stocks['High_EMA'] = stocks['High'].ewm(span = 50, adjust = False).mean()
    stocks['Low_EMA'] = stocks['Low'].ewm(span = 50, adjust = False).mean()
    # stocks = stocks.groupby(stocks.index.strftime('%Y-%m-%d %H:00')).mean()
    stocks['Datetime'] = stocks.index.map(str)

    return stocks.to_dict('list')
