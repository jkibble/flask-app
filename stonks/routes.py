from stonks import app, db, Todo
from flask import render_template, request, redirect
import json

from .stonks import stonks

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search  = request.get_json()['search']
    tickers = stonks.tickerSearch(search)

    return { 'tickers': tickers }

@app.route('/select/<ticker>')
def calculate(ticker):
    info = stonks.getCompanyInfo(ticker)
    stocks = stonks.getStonks(ticker)

    return { 'company': info, 'stocks': stocks }
