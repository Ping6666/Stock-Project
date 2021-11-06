# Stock-Project

## Usage

Web Crawl the stock historical price from Goodinfo, TWSE, YahooFinance. \
Then pre-process the raw data to structured data CSV, post-process the result with technical analysis. \
Use Plotly to show the data from CSV file.

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

### ./v0.1_Crawler/dataCrawler_Goodinfo.py

> IP limit: about 15
> dynamic webcrawler

- [技術分析 - 日K線圖暨股價漲跌資料表 - Goodinfo!台灣股市資訊網](https://goodinfo.tw/StockInfo/ShowK_Chart.asp)

### ./v0.1_Crawler/dataCrawler_TWSE.py

> IP limit: about 25

- [個股日成交資訊TWSE 臺灣證券交易所](https://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html)

### ./v0.4/dataCrawler_YahooFinance.py

> IP limit: 695

- [Yahoo Finance - Stock Market Live, Quotes, Business & Finance News](https://finance.yahoo.com/)
- [TAIWAN SEMICONDUCTOR MANUFACTUR (2330.TW) Stock Historical Prices & Data - Yahoo Finance](https://finance.yahoo.com/quote/2330.TW/history?p=2330.TW)

### Related Project

[Program 2 - Threading Programming](https://github.com/Ping6666/Operating-System-Projects/blob/main/Program%202%20-%20Threading%20Programming/README.md)

## CLI

mainProcess.py [-a fileType] [-p] [-i fileName] [-l timeLength]

### File Bases

- `./rawData/`
- `./postData/`
- `./stockNumber/`

### Input File Name

- `.asp`: `ShowBuySaleChartData-stockNum.asp`
- `.html`: `K_Chart-stockNum-yymmdd.html`
- `.csv`: `stockNum.csv`
- `.txt`: `stock.txt`

## PreProcess

> Python Package: [Welcome to Technical Analysis Library in Python’s documentation! — Technical Analysis Library in Python 0.1.4 documentation](https://technical-analysis-library-in-python.readthedocs.io/en/latest/)

### Index (Technical  Analysis, Chip Analysis)

- Date, Open, High, Low, Close, Volume

* Foreign, Trust, Dealer, ForeignRatio

- RSI
- KD
- KC
- SMA
- Ichimoku Cloud

## PostProcess

Calculate Score and save rank result to a single CSV file

## Visualize Data

> Tool: [Plotly Python Graphing Library | Python | Plotly](https://plotly.com/python/)

