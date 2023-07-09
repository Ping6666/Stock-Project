from typing import List
from io import StringIO

import pathlib

import requests
from fake_useragent import UserAgent

import numpy as np
import pandas as pd
from ta import momentum, trend, volatility

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

    # --- KC --- #

    _kc = volatility.KeltnerChannel(high=df['High'],
                                    low=df['Low'],
                                    close=df['Close'])
    _kc_high = _kc.keltner_channel_hband()
    _kc_middle = _kc.keltner_channel_mband()
    _kc_low = _kc.keltner_channel_lband()

    # --- SMA --- #

    _windows = [5, 10, 20, 60, 120, 240]
    _smas = []
    for _window in _windows:
        _sma = trend.SMAIndicator(close=df['Close'], window=_window)
        _smas.append(_sma.sma_indicator())

    # --- Ichimoku Cloud --- #

    _ich = trend.IchimokuIndicator(high=df['High'], low=df['Low'], visual=True)
    _ich_a = _ich.ichimoku_a()
    _ich_b = _ich.ichimoku_b()
    _ich_base_line = _ich.ichimoku_base_line()
    _ich_conversion_line = _ich.ichimoku_conversion_line()

    ## -- plot convert -- ##

    def shift_list(seq, n):
        return seq[n:]

    _ich_plot_1 = ((df['Close'] - _ich_conversion_line) +
                   (df['Close'] - _ich_base_line))
    _ich_plot_2 = (_ich_a - _ich_b)

    displacement = 26
    ich_tmp_1 = shift_list(_ich_a, displacement - 1)
    ich_tmp_2 = shift_list(_ich_b, displacement - 1)
    ich_tmp_1 = df["Close"] - ich_tmp_1
    ich_tmp_2 = df["Close"] - ich_tmp_2

    _ich_plot_3 = []
    for idx in range(len(ich_tmp_1)):
        new_a = ich_tmp_1[idx]
        new_b = ich_tmp_2[idx]

        # magnitude
        _new = min(abs(new_a), abs(new_b))

        # sign
        tmp_sign = 0
        if new_a > 0 and new_b > 0:
            tmp_sign = 1
        elif new_a < 0 and new_b < 0:
            tmp_sign = -1

        _ich_plot_3.append(_new * tmp_sign)

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
        'KC_high': _float_list(_kc_high),
        'KC_middle': _float_list(_kc_middle),
        'KC_low': _float_list(_kc_low),
        'ICH_plot_1': _float_list(_ich_plot_1),
        'ICH_plot_2': _float_list(_ich_plot_2),
        'ICH_plot_3': _float_list(_ich_plot_3),
        'SMA_5': _float_list(_smas[0]),
        'SMA_10': _float_list(_smas[1]),
        'SMA_20': _float_list(_smas[2]),
        'SMA_60': _float_list(_smas[3]),
        'SMA_120': _float_list(_smas[4]),
        'SMA_240': _float_list(_smas[5]),
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
            'KC_high': df['KC_high'].iloc[-1],
            'KC_middle': df['KC_middle'].iloc[-1],
            'KC_low': df['KC_low'].iloc[-1],
            'ICH_plot_1': df['ICH_plot_1'].iloc[-1],
            'ICH_plot_2': df['ICH_plot_2'].iloc[-1],
            'ICH_plot_3': df['ICH_plot_3'].iloc[-1],
            'SMA_5': df['SMA_5'].iloc[-1],
            'SMA_10': df['SMA_10'].iloc[-1],
            'SMA_20': df['SMA_20'].iloc[-1],
            'SMA_60': df['SMA_60'].iloc[-1],
            'SMA_120': df['SMA_120'].iloc[-1],
            'SMA_240': df['SMA_240'].iloc[-1],
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
        'KC_high',
        'KC_middle',
        'KC_low',
        'ICH_plot_1',
        'ICH_plot_2',
        'ICH_plot_3',
        'SMA_5',
        'SMA_10',
        'SMA_20',
        'SMA_60',
        'SMA_120',
        'SMA_240',
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
