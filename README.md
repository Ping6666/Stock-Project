# stock project

version: v1.0.1

## Usage

Web Crawl the stock historical price from Goodinfo (deprecate since v0.7), TWSE (deprecate since v0.7), YahooFinance. \
Then pre-process the raw data to structured data CSV, post-process the result with technical analysis. \
Use Plotly to show the data from CSV file.

### Warning on Web Crawl

Please know that the data from the website which being web crawled may include some contents that are being copyright law protected. \
If you are trying to use this code against the copyright law where you are or the web server is, you will have to take full responsabilities.

## Start-up

### With Docker (& Docker compose)

- (sudo) docker network create web_service
- (sudo) docker compose up [-d]
- just have fun on `0.0.0.0:5000`

### Without Docker

- virtualenv (option)
- copy stock-project folder into new (venv) folder
- change directory to folder $your_path/stock/
- activate current venv (option) & pip install -r requirements.txt
- run [export PYTHONPATH="$PYTHONPATH:./core"]
- run [python ./backend/main.py]
- just have fun on `0.0.0.0:5000`

## Code Walkthrough

### core/dataCrawler: YahooFinance

> IP limit: 695

#### web api

- [Yahoo Finance - Stock Market Live, Quotes, Business & Finance News](https://finance.yahoo.com/)
- [TAIWAN SEMICONDUCTOR MANUFACTUR (2330.TW) Stock Historical Prices & Data - Yahoo Finance](https://finance.yahoo.com/quote/2330.TW/history?p=2330.TW)

### core/preProcess

> Python Package - TA: [Welcome to Technical Analysis Library in Python’s documentation!](https://technical-analysis-library-in-python.readthedocs.io/en/latest/)

#### index (technical  analysis, chip analysis)

- Date, Open, High, Low, Close, Volume

* Foreign, Trust, Dealer, ForeignRatio

- RSI
- KD
- KC
- SMA
- Ichimoku Cloud

### core/postProcess

Calculate score and save rank result to a single CSV file

### backend/main

- ployly (with dash and flask)

> Tool: [Plotly Python Graphing Library | Python | Plotly](https://plotly.com/python/)

## License

plz follow MIT License
