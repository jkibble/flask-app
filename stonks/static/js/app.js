const app = new Vue({
  el: '#app',

  data: {
    ticker: '',
    tickers: [],
    options: {
      tickers: '',
      short: 5,
      long: 10,
      timeframe: '15m',
      movingAverage: 'RSI',
      dayScale: 0
    }
  },

  mounted() {
    this.selectStock('gme rkt qqq');
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
    }
  }
});
