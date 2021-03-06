from datetime import datetime, timedelta

import pandas as pd
from pandas_datareader import data as pdr

class YahooClient:
    def __init__(self):
        self.api = pdr

    def getStocks(self, symbols, timeframe='5Min', limit=30):
        aggregate = []
        start = datetime.today() - timedelta(days = limit)
        end = datetime.today()

        df = self.api.DataReader(symbols, 'yahoo', start = start, end = end)

        for symbol in symbols:
            data = pd.DataFrame(data={
                'time': df.index.strftime('%Y-%m-%d %H:%M:%S'),
                'close': df['Close'][symbol],
            })

            data['symbol'] = symbol

            aggregate.append(data)

        return pd.concat(aggregate)
