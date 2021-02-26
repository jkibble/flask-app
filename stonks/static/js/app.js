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
    svg: {},
    x: {},
    y: {},
    line: {},
    thing: ''
  },

  mounted() {
    const el = document.querySelector('#graph1');
    let self = this;

    this.width = el.offsetWidth;
    this.height = el.offsetHeight;

    this.initalizeGraph();

    this.selectStock({ symbol: 'AAPL', name: 'Apple' });
  },

  methods: {
    selectStock(ticker) {
      let self = this;

      self.companyName = ticker.name

      fetch(`/select/${ticker.symbol}`)
        .then(response => response.json())
        .then(data => {
          self.companyInfo = data.company;
          self.stocks = data.stocks;

          this.addLine(this.formatData('Close'), 'red');
          this.addLine(this.formatData('Open'), 'blue');
          this.addLine(this.formatData('previous7dayhigh'), 'goldenrod');
          this.addLine(this.formatData('previous7daylow'), 'black');
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    },

    addLine(data, colour) {
      this.x.domain(d3.extent(data, d => d.date))
      this.y.domain([0, d3.max(data, d => d.value)])

      this.svg.append('path')
        .attr('fill', 'none')
        .attr('stroke', colour)
        .attr('stroke-width', 1.5)
        .attr('d', this.line(data));
    },

    initalizeGraph() {
      // this.svg.remove();

      this.svg = d3.select('#graph1').append('svg');

      this.svg.attr('width', this.width)
        .attr('height', this.height)
        .append('g');

      let x = d3.scaleUtc().range([0, this.width]);
      let y = d3.scaleLinear().range([this.height, 0]);

      let line = d3.line()
        .defined(d => !isNaN(d.value))
        .x(d => x(d.date))
        .y(d => y(d.value));

      let xAxis = d3.axisBottom(x).tickFormat(d3.timeFormat('%b %d'));
      let yAxis = d3.axisLeft(y);

      let focus = this.svg.append('g').attr('transform', 'translate(20, 20)');
      focus.append('g').attr('transform', `translate(0, ${this.height - 30})`).call(xAxis);
      focus.append('g').call(yAxis);

      this.x = x;
      this.y = y;
      this.line = line;
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
          date: new Date(date),
          value: self.stocks[column][index]
        }
      });
    }
  }
});
