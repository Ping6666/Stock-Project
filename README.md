# Stock-Project

## Usage

Web Crawl the stock historical price from Goodinfo, TWSE, YahooFinance. \
Then pre-process the raw data to structured data CSV, post-process the result with technical analysis. \
Use Plotly to show the data from CSV file.

### Easy use

1. edit `.txt` under stockNumber
2. run python` mainProcess.py -i {%fileName}`
3. run flask or supervisor (uwsgi, nginx)
4. if using supervisor end with `.sh`

## Necessary Packages

- `ta` == 0.7.0
  - `pandas` == 1.2.4
  - `numpy` == 1.20.3
- `dash` == 1.20.0
- `requests` == 2.26.0
- `fake_useragent` == 0.1.11
- `lxml` == 4.6.3

## Web Crawl Source

### Warning

Please know that the data from the website which being web crawled may include some contents that are being copyright law protected.
If you are trying to use this code against the copyright law where you are or the web server is, you will have to take full responsabilities.

### `./src/dataCrawler_Goodinfo.py`

> IP limit: about 15
> dynamic webcrawler

- [技術分析 - 日K線圖暨股價漲跌資料表 - Goodinfo!台灣股市資訊網](https://goodinfo.tw/StockInfo/ShowK_Chart.asp)

### `./src/dataCrawler_TWSE.py`

> IP limit: about 25

- [個股日成交資訊TWSE 臺灣證券交易所](https://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html)

### `./src/dataCrawler_YahooFinance.py`

> IP limit: 695

- [Yahoo Finance - Stock Market Live, Quotes, Business & Finance News](https://finance.yahoo.com/)
- [TAIWAN SEMICONDUCTOR MANUFACTUR (2330.TW) Stock Historical Prices & Data - Yahoo Finance](https://finance.yahoo.com/quote/2330.TW/history?p=2330.TW)

## Supervisor

update soon

## Nginx

update soon

## uWSGI

update soon

## CLI

mainProcess.py [-a fileType] [-p] [-i fileName] \
visualizeData.py

### `mainProcess.py -a {%fileName}`

pre-process all files which is either `.asp`, `.html` or `.csv` and in base file dir (`../rawData/`)

### `mainProcess.py -i {%fileName}`

pre-process single file which is either `.asp`, `.html` or `.csv`
web crawle from Yahoo Finance website according to stock list in `.txt` (txt base file dir: `../stockNumber/`)

### `mainProcess.py -p`

post-process all `.csv` in base file dir (`../postData/`)

### `visualizeData.py`

run flask (without uwsgi, nginx)

## file hierarchy

### file bases

- `./rawData/`
- `./postData/`
- `./stockNumber/`

### input file name

- `.asp`: `ShowBuySaleChartData-stockNum.asp`
- `.html`: `K_Chart-stockNum-yymmdd.html`
- `.csv`: `stockNum.csv`
- `.txt`: `stock.txt`

## src

### preProcess

> Python Package: [Welcome to Technical Analysis Library in Python’s documentation!](https://technical-analysis-library-in-python.readthedocs.io/en/latest/)

#### index (technical  analysis, chip analysis)

- Date, Open, High, Low, Close, Volume

* Foreign, Trust, Dealer, ForeignRatio

- RSI
- KD
- KC
- SMA
- Ichimoku Cloud

### postProcess

Calculate Score and save rank result to a single CSV file

### visualizeData

> Tool: [Plotly Python Graphing Library | Python | Plotly](https://plotly.com/python/)

## License

plz follow MIT License
