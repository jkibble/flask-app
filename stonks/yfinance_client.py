import pandas as pd
import yfinance as yf

class YfinanceClient:
    def __init__(self):
        self.api = yf

    def getStocks(self, symbols, timeframe='5m', limit=30):
        aggregate = []
        df = self.api.download(symbols, period='1mo', interval=timeframe)

        if len(symbols) == 1:
            data = pd.DataFrame(data={
                'time': df.index.strftime('%Y-%m-%d %H:%M:%S'),
                'close': df['Close'],
            })

            data['symbol'] = symbols[-1]

            return data
        else:
            for symbol in symbols:
                data = pd.DataFrame(data={
                    'time': df.index.strftime('%Y-%m-%d %H:%M:%S'),
                    'close': df['Close'][symbol],
                })

                data['symbol'] = symbol

                aggregate.append(data)

        return pd.concat(aggregate)
