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
    stocks = scraper.getStonks(options['tickers'], options['short'], options['long'], options['timeframe'], options['movingAverage'], options['dayScale'])
    interval = alt.selection_interval(encodings=['x'])
    selection = alt.selection_multi(fields=['symbol'], bind='legend')

    print(stocks)

    base = alt.Chart(stocks).encode(
        x=alt.X('yearmonthdatehoursminutes(time):O', axis = alt.Axis(title = 'Date'.upper(), format = ('%b %d %H:%M'))),
        color='symbol:N',
        opacity=alt.condition(selection, alt.value(0.5), alt.value(0.1))

    ).properties(
        width=1200,
        height=550
    )

    close = base.mark_line(
        point=True
    ).encode(
        y='close:Q',
        tooltip='close:Q',
    ).add_selection(
        interval,
        selection
    )

    sell = base.mark_point(
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

    buy = base.mark_point(
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

    area = base.mark_area(
        opacity=0.3
    ).encode(
        y='short:Q',
        y2='long:Q',
    )

    chart = close + buy + sell + area

    return chart.to_dict()
