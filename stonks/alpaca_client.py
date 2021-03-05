import alpaca_trade_api as tradeapi
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

api = tradeapi.REST()

def getAlpacaStocks(symbols, timeframe='5Min', limit=30):
    df = api.get_barset(symbols=symbols, timeframe=timeframe, limit=limit).df

    aggregate = []

    for symbol in symbols:
        data = pd.DataFrame(data={
            'time': df.index.strftime('%Y-%m-%d %H:%M:%S'),
            'close': df[symbol]['close'],
        })

        data['symbol'] = symbol

        aggregate.append(data)

    return pd.concat(aggregate)
