from typing import List
from io import StringIO

import pathlib

import requests
from fake_useragent import UserAgent

import numpy as np
import pandas as pd
from ta import momentum

# The sample of Yahoo Finance website url
# 'https://query1.finance.yahoo.com/v7/finance/download/2330.TW?period1=946944000&period2=1627603200&interval=1d&events=history&includeAdjustedClose=true'
# 2330.TW
# 2000/01/04 - 2021/07/30 (不含 07/30) : 6032 - 5168 = 864 (/天)
# 'https://query1.finance.yahoo.com/v7/finance/download/2330.TW?period1=946944000&period2=1627516800&interval=1d&events=history&includeAdjustedClose=true'
# 2330.TW
# 2000/01/04 - 2021/07/29 (不含 07/29) : 5168 - 4304 = 864 (/天)
# 'https://query1.finance.yahoo.com/v7/finance/download/2330.TW?period1=947030400&period2=1627430400&interval=1d&events=history&includeAdjustedClose=true'
# 2330.TW
# 2000/01/05 - 2021/07/28 (不含 07/28)
# 'https://query1.finance.yahoo.com/v7/finance/download/3481.TW?period1=1161648000&period2=1627516800&interval=1d&events=history&includeAdjustedClose=true'
# 3481.TW
# 2006/10/24 - 2021/07/29

# period1 可以給 小於最早日期 例如          0 (代表輸出 需涵蓋最舊資料)
# period2 可以給 大於最新日期 例如 2000000000 (代表輸出 需涵蓋最新資料)


def _float(inputNum):
    if inputNum != 'null' and not np.isnan(inputNum):
        return True
    return False


def _float_list(l):
    return [float(i) if _float(i) else 0 for i in l]


def _str_list(l):
    return [str(i).replace('-', '/') for i in l]


def file_reader(_filename: str):
    symbols = []

    try:
        _str = ''
        with open(_filename, 'r', encoding='utf-8') as f:
            _str = f.read()

        symbols = _str.split('\n')

    except Exception as e:
        print(e)

    return symbols


def symbol_parser(symbols: List[str]):

    parsed_symbols = []
    try:
        for _symbol in symbols:

            symbol = _symbol.strip()
            if symbol == '' or symbol[0] == '#':
                continue

            parsed_symbols.append(symbol)

    except Exception as e:
        print(e)

    return parsed_symbols


def _preprocess_ta(df):
    # --- RSI, KD --- #

    __rsi = momentum.RSIIndicator(close=df['Close'])
    _kd = momentum.StochasticOscillator(high=df['High'],
                                        low=df['Low'],
                                        close=df['Close'])
    _k = _kd.stoch()
    _d = _kd.stoch_signal()

    _rsi = __rsi.rsi()

    _k_rsi = _rsi * _k / 100
    _d_rsi = _rsi * _d / 100

    # --- pd.DataFrame --- #

    _df = pd.DataFrame({
        'Date': df['Date'],
        'Open': df['Open'],
        'High': df['High'],
        'Low': df['Low'],
        'Close': df['Close'],
        'Volume': df['Volume'],
        'K': _float_list(_k),
        'D': _float_list(_d),
        'RSI': _float_list(_rsi),
        'K_RSI': _float_list(_k_rsi),
        'D_RSI': _float_list(_d_rsi),
    })

    return _df


def _preprocess(df):

    _df = pd.DataFrame({
        'Date': _str_list(df['Date']),
        'Open': _float_list(df['Open']),
        'High': _float_list(df['High']),
        'Low': _float_list(df['Low']),
        'Close': _float_list(df['Close']),
        'Volume': _float_list(df['Volume']),
    })

    # --- magic check --- #

    checker = []
    for i in range(len(_df)):
        a = _df['Open'].iloc[i] == 0
        b = _df['High'].iloc[i] == 0
        c = _df['Low'].iloc[i] == 0
        d = _df['Close'].iloc[i] == 0
        e = _df['Volume'].iloc[i] == 0

        if (a and b and c and d and e):
            checker.append(i)

    if ((len(_df) - len(checker)) <= 1):
        print(f'Data wrong at date with the amount: {len(checker)}.')

    # --- process --- #

    _df.drop(index=checker, inplace=True)
    _df.reset_index(inplace=True, drop=True)

    return _df


def download_yahoo_finance(symbol: str, save_path: str, _interval: str = '1d'):
    '''
    Args:
        _interval: '1d', '1wk', '1mo'

    '''

    df = None
    try:
        print(f'symbol {symbol}, interval {_interval}', end=' ')

        ua = UserAgent()
        userAgent = ua.random
        headers = {'User-Agent': userAgent}

        urlBase = (
            f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}' +
            f'?period1=0&period2=2000000000&interval={_interval}' +
            '&events=history&includeAdjustedClose=true')

        # -- load from the website -- #

        res = requests.get(urlBase, headers=headers)
        res_ctx = res.content

        # -- decode -- #

        res_ctx_decode = str(res_ctx, 'utf-8', errors='ignore')
        raw_data = StringIO(res_ctx_decode)
        df = pd.read_csv(raw_data)

        df = _preprocess(df)
        df = _preprocess_ta(df)

        # -- save -- #

        df.to_csv(save_path, index=False)
        print('done')

    except Exception as e:
        print(e)

    return


def _postprocess(_filename: str):

    _post = {}
    try:
        df = pd.read_csv(_filename)

        _post = {
            'Name': pathlib.Path(_filename).name,
            'Date': df['Date'].iloc[-1],
            'Open': df['Open'].iloc[-1],
            'High': df['High'].iloc[-1],
            'Low': df['Low'].iloc[-1],
            'Close': df['Close'].iloc[-1],
            'Volume': df['Volume'].iloc[-1],
            'K': df['K'].iloc[-1],
            'D': df['D'].iloc[-1],
            'RSI': df['RSI'].iloc[-1],
            'K_RSI': df['K_RSI'].iloc[-1],
            'D_RSI': df['D_RSI'].iloc[-1],
        }

    except Exception as e:
        print(e)

    return _post


def postprocess(_files: List[str], save_path: str):

    columns = [
        'Name',
        'Date',
        'Open',
        'High',
        'Low',
        'Close',
        'Volume',
        'K',
        'D',
        'RSI',
        'K_RSI',
        'D_RSI',
    ]
    _datas = []

    for _file in _files:
        _data = _postprocess(_file)

        if _data is not None and _data != {}:
            _datas.append(_data)

    df = pd.DataFrame(_datas, columns=columns)

    # --- save --- #

    df.to_csv(save_path, index=False)
    print('done')

    return
