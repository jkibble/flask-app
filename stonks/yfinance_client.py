from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf

def getYFinanceStocks(symbols, timeframe='5m', limit=30):
    aggregate = []
    df = yf.download(symbols, period='1d', interval=timeframe)

    for symbol in symbols:

        # ticker = yf.Ticker(symbol)
        # df = ticker.history(period='1d', interval=timeframe.lower())

        data = pd.DataFrame(data={
            'time': df.index.strftime('%Y-%m-%d %H:%M:%S'),
            'close': df['Close'][symbol],
        })

        data['symbol'] = symbol

        aggregate.append(data)

    return pd.concat(aggregate)
