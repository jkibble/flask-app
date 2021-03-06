from stonks import app
from flask import render_template, request
import altair as alt

import stonks.stock_calc as Stocks

scraper = Stocks.Stonks()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search = request.get_json()['search']
    tickers = scraper.tickerSearch(search)

    return {'tickers': tickers}


@app.route('/select-stocks', methods=['POST'])
def calculate():
    options = request.get_json()
    stocks = scraper.getStonks(options['tickers'], options['short'], options['long'], options['timeframe'], options['movingAverage'])
    interval = alt.selection_interval(encodings=['x'])
    selection = alt.selection_multi(fields=['symbol'], bind='legend')

    print(stocks)

    close = alt.Chart(
        stocks
    ).mark_line(
        point=True
    ).encode(
        x='time:T',
        y='close:Q',
        color='symbol:N',
        tooltip='change:Q',
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
    ).properties(
        width=1200,
        height=550
    ).add_selection(
        interval,
        selection
    )

    sell = alt.Chart(stocks).mark_point(
        filled=True,
        size=200,
        shape='triangle-down',
        color='red',
        opacity=0.5
    ).encode(
        x='time:T',
        y='sell:Q',
        tooltip='close:Q'
    )

    buy = alt.Chart(stocks).mark_point(
        filled=True,
        size=200,
        shape='triangle-up',
        color='green',
        opacity=0.5
    ).encode(
        x='time:T',
        y='buy:Q',
        tooltip='close:Q'
    )

    area = alt.Chart(stocks).mark_area(
        opacity=0.3
    ).encode(
        x='time:T',
        y='short:Q',
        y2='long:Q',
        color='symbol:N',
        opacity=alt.condition(selection, alt.value(0.5), alt.value(0.1))
    )

    chart = close + buy + sell + area

    return chart.to_dict()
