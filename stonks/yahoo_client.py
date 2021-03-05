from datetime import datetime, timedelta

import pandas as pd
from pandas_datareader import data as pdr

def getYahooStocks(symbols, timeframe='5Min', limit=30):
    aggregate = []
    start = datetime.today() - timedelta(days = limit)
    end = datetime.today()

    for symbol in symbols:
        df = pdr.DataReader(symbol, 'yahoo', start = start, end = end)

        data = pd.DataFrame(data={
            'time': df.index.strftime('%Y-%m-%d %H:%M:%S'),
            'close': df['Close'],
        })

        data['symbol'] = symbol

        aggregate.append(data)

    return pd.concat(aggregate)
