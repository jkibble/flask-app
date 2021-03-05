const app = new Vue({
  el: '#app',

  data: {
    ticker: '',
    tickers: [],
    stocks: {
      Datetime: [],
    },
    options: {
      tickers: '',
      short: 10,
      long: 20,
      timeframe: '5m',
      movingAverage: 'SMA'
    }
  },

  mounted() {
    this.selectStock('gme yolo tsla msft lyft');
  },

  methods: {
    selectStock(symbol) {
      let self = this;
      self.options.tickers = symbol
      self.tickers = [];

      document.querySelector('#graph1').innerHTML = '<img class="center" src="https://wpamelia.com/wp-content/uploads/2018/11/ezgif-2-6d0b072c3d3f.gif">'

      fetch(`/select-stocks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.options)
      })
        .then(response => response.json())
        .then(data => {

          vegaEmbed('#graph1', data);
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    },

    searchTicker() {
      let self = this;

      fetch('/search', {
        method: 'POST', // or 'PUT'
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ search: this.ticker }),
      })
        .then(response => response.json())
        .then(data => {
          self.tickers = data.tickers;
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    },

    formatData(column) {
      let self = this;

      return this.stocks.Datetime.map(function (date, index) {
        return {
          t: new Date(date),
          x: self.stocks[column][index]
        }
      });
    }
  }
});
