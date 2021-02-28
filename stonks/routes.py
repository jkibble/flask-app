from stonks import app
from flask import render_template, request
import altair as alt

from .stonks import stonks


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    search = request.get_json()['search']
    tickers = stonks.tickerSearch(search)

    return {'tickers': tickers}


@app.route('/select/<ticker>', methods=['POST', 'GET'])
def calculate(ticker):
    info = stonks.getCompanyInfo(ticker)
    options = request.get_json()
    stocks = stonks.getStonks(ticker, options['short'], options['long'], options['days'], options['money'])
    interval = alt.selection_interval(encodings=['x'])

    print(stocks)

    close = alt.Chart(stocks).transform_fold(
        ['Close', 'Short', 'Long'],
        as_=['Status', 'Price']
    ).mark_line().encode(
        x='Datetime:T',
        y='Price:Q',
        color='Status:N'
    ).properties(
        width=1200,
        height=600
    ).add_selection(interval)


    sell = alt.Chart(stocks).mark_text().encode(
        x='Datetime:T',
        y='Sell:Q',
        text=alt.value('Sell!'),
        tooltip='Close:Q'
    )

    buy = alt.Chart(stocks).mark_text().encode(
        x='Datetime:T',
        y='Buy:Q',
        text=alt.value('Buy!'),
        tooltip='Close:Q'
    )

    fill = alt.Chart(stocks).mark_area(color='#ADCCFF', opacity=0.3).encode(
        x='Datetime:T',
        y='Short:Q',
        y2='Long:Q'
    )

    # rule = alt.Chart(stocks).mark_rule(color='red').encode(
    #     y='Sell:Q'
    # )

    chart = close + sell + buy + fill

    return {'company': info, 'chart': chart.to_dict()}
