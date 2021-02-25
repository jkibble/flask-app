const app = new Vue({
  el: '#app',

  data: {
    ticker: '',
    tickers: [],
    companyName: '',
    companyInfo: {},
    stocks: {
      Datetime: [],
    },
    width: 0,
    height: 0,
    svg: ''
  },

  mounted() {
    const el = document.querySelector('#graph1');

    this.width = el.offsetWidth;
    this.height = el.offsetHeight;

    d3.select("body")
      .append("svg")
      .attr("width", this.width)
      .attr("height", this.height);


    this.selectStock({ symbol: 'TSLA', name: 'Tesla!!!' });
  },

  methods: {
    selectStock(ticker) {
      let self = this;

      self.companyName = ticker.name
      self.stocks.Datetime = [];

      fetch(`/select/${ticker.symbol}`)
        .then(response => response.json())
        .then(data => {
          self.companyInfo = data.company;
          self.stocks = data.stocks;
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

    getLinePath(lineData) {
      let x = d3.scaleTime().range([0, this.width]); // width
      let y = d3.scaleLinear().range([this.height, 0]); // height
      let line = d3.line()
        .x(function (d) { return x(d.date); })
        .y(function (d) { return y(d.value); });

      x.domain([d3.min(lineData, d => d.date), d3.max(lineData, d => d.date)])
      y.domain([d3.min(lineData, d => d.value), d3.max(lineData, d => d.value)])

      return line(lineData);
    }
  },

  computed: {
    closePath() {
      let self = this;
      let lineData = []

      self.stocks.Datetime.forEach(function (date, index) {
        lineData.push({
          date: new Date(date),
          value: self.stocks.Close[index]
        })
      });

      return this.getLinePath(lineData)
    },

    openPath() {
      let self = this;
      let lineData = []

      self.stocks.Datetime.forEach(function (date, index) {
        lineData.push({
          date: new Date(date),
          value: self.stocks.Open[index]
        })
      });

      return this.getLinePath(lineData)
    }
  }
});
