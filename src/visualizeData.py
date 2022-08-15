# version: 0.6

# take out data from csv file and then visualize the data
import os, sys
import pandas as pd
import numpy as np
from datetime import date

pd.options.display.float_format = '{:.3f}'.format

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def graphFromFile(fileBase, fileName, timeLength_):
    # data in and process the date
    if '.csv' not in fileName:
        fileName = fileBase + fileName + '.csv'
    showingName = str(fileName.split('/')[-1])
    showingName = showingName.replace('.csv', '')
    try:
        df = pd.read_csv(fileName)
    except:
        print("No such file or directory : " + fileName)
        exit(1)
    # take out the chinese name of cc = TW stock
    stockNameList = '../stockNumber/TW_all.txt'
    if showingName.find('.TW') != 0:
        try:
            f = open(stockNameList, 'r', encoding='utf-8')
        except:
            print("No such file or directory : " + stockNameList + ".")
        tmpList = f.readlines()
        tmpList_ = []
        for tmp in tmpList:
            tmp_ = tmp.replace('\n', '')
            tmp_ = tmp_.split(' ')[0]
            tmpList_.append(tmp_)
        f.close()
        stockNumber = showingName.split('.')[0]
        for i in range(len(tmpList_)):
            if stockNumber == (tmpList_[i].split('\t')[0]):
                showingName = tmpList_[i].split('\t')[-1] + " " + showingName
                break
    timeLength_ = min(timeLength_, len(df))
    # for check volume low point
    checkLen = 60
    timeLengthTmp = min(timeLength_ + checkLen + 1, len(df))
    df_ = df[-timeLengthTmp:]
    # end
    df = df[-timeLength_:]
    dtAll = pd.date_range(start=df['Date'].iloc[0], end=df['Date'].iloc[-1])
    dtAll = dtAll.strftime("%Y/%m/%d")
    dtBreaks = [d for d in dtAll if d not in df['Date'].tolist()]
    # csv : Date, Open, High, Low, Close, Volume, KC, KD * RSI, 外資, 投信, 自營商, 外資持股比率, 股東持股分級
    ## start of fig
    # set the graph be subplot type
    fig = make_subplots(
        rows=7,
        cols=1,
        row_heights=[0.4, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
        vertical_spacing=0.05,
        shared_xaxes=True,
        subplot_titles=(
            "Candlestick Charts",
            "Score (high: buy, low: sell)",
            # "Trend Analysis (>0 漲勢, =0 平盤, <0 跌勢)",
            "KD*RSI",
            "Ichimoku Indicator",
            "Volume",
            "Chip Analysis",
            "Foreign Chip Ratio"))
    # set 1st plot in the subplot - 1st line (Stock Price)
    fig.add_trace(
        go.Candlestick(x=df['Date'],
                       open=df['Open'],
                       high=df['High'],
                       low=df['Low'],
                       close=df['Close'],
                       name="Candlestick"), 1, 1)
    # set 1st plot in the subplot - 2nd line (Keltner Channel)
    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df['KC_high'],
                   name="KC-H",
                   visible='legendonly'), 1, 1)
    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df['KC_middle'],
                   name="KC-M",
                   visible='legendonly'), 1, 1)
    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df['KC_low'],
                   name="KC-L",
                   visible='legendonly'), 1, 1)
    # set 1st plot in the subplot - 3nd line (MA)
    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df['SMA_5'],
                   name="SMA-5",
                   visible='legendonly'), 1, 1)
    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_10'], name="SMA-10"), 1,
                  1)
    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df['SMA_20'],
                   name="SMA-20",
                   visible='legendonly'), 1, 1)
    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df['SMA_60'],
                   name="SMA-60",
                   visible='legendonly'), 1, 1)
    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df['SMA_120'],
                   name="SMA-120",
                   visible='legendonly'), 1, 1)
    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df['SMA_240'],
                   name="SMA-240",
                   visible='legendonly'), 1, 1)
    # set 2nd plot in the subplot
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Score'], name="Score"), 2, 1)
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['Score_SMA_5'], name="Score SMA-5"), 2,
        1)
    # fig.add_trace(
    #     go.Scatter(x=df['Date'], y=df['ScorePoint'], name="ScorePoint"), 2, 1)
    fig.add_shape(dict(type="line",
                       x0=0,
                       x1=timeLength_,
                       y0=-30,
                       y1=-30,
                       line_color="black"),
                  row=2,
                  col=1)
    fig.add_shape(dict(type="line",
                       x0=0,
                       x1=timeLength_,
                       y0=0,
                       y1=0,
                       line_color="black"),
                  row=2,
                  col=1)
    fig.add_shape(dict(type="line",
                       x0=0,
                       x1=timeLength_,
                       y0=30,
                       y1=30,
                       line_color="black"),
                  row=2,
                  col=1)
    totalLen1, totalLen2 = len(df['Date']), len(df_['Date'])
    for i in range(totalLen1):
        if i == totalLen1 - 1:
            continue
        if i < totalLen2:
            checkNowLow = df_['Volume'].iloc[-i - 1]
            if checkNowLow != 0:
                checkResult = True
                for j in range(checkLen - 1):
                    j_ = j + 1
                    checkTmp = 0
                    if i + j_ < totalLen2 and checkResult:
                        checkTmp = df_['Volume'].iloc[-i - 1 - j_]
                        if checkTmp != 0 and checkTmp < checkNowLow:
                            # Bad
                            checkResult = False
                if checkResult:
                    fig.add_vline(x=df_['Date'].iloc[-i - 1],
                                  line_width=1,
                                  line_dash="dash",
                                  line_color="green",
                                  row=2,
                                  col=1)
            checkNowHigh = df_['Volume'].iloc[-i - 1]
            if checkNowHigh != 0:
                checkResult = True
                for j in range(checkLen - 1):
                    j_ = j + 1
                    checkTmp = 0
                    if i + j_ < totalLen2 and checkResult:
                        checkTmp = df_['Volume'].iloc[-i - 1 - j_]
                        if checkTmp != 0 and checkTmp > checkNowHigh:
                            # Bad
                            checkResult = False
                if checkResult:
                    fig.add_vline(x=df_['Date'].iloc[-i - 1],
                                  line_width=1,
                                  line_dash="dash",
                                  line_color="red",
                                  row=2,
                                  col=1)
    # set 3rd plot in the subplot - Trend Analysis
    # fig.add_trace(go.Scatter(x=df['Date'], y=df['TrendAnalysis'], name="TA"),
    #               3, 1)
    # fig.add_trace(
    #     go.Scatter(x=df['Date'], y=df['TrendAnalysisRaw'], name="TA-R"), 3, 1)
    # set 3rd plot in the subplot - KD*KSI
    fig.add_trace(go.Scatter(x=df['Date'], y=df['K'], name="K*RSI"), 3, 1)
    fig.add_trace(go.Scatter(x=df['Date'], y=df['D'], name="D*RSI"), 3, 1)
    fig.add_shape(dict(type="line",
                       x0=0,
                       x1=timeLength_,
                       y0=10,
                       y1=10,
                       line_color="black"),
                  row=3,
                  col=1)
    fig.add_shape(dict(type="line",
                       x0=0,
                       x1=timeLength_,
                       y0=70,
                       y1=70,
                       line_color="black"),
                  row=3,
                  col=1)
    # set 4th plot in the subplot - Ichimoku Clouds
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['ICH_plot_1'], name="Rise_Potential"), 4,
        1)
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['ICH_plot_2'], name="Cloud_Protection"),
        4, 1)
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['ICH_plot_3'], name="Cloud_Distance"), 4,
        1)
    fig.add_shape(dict(type="line",
                       x0=0,
                       x1=timeLength_,
                       y0=0,
                       y1=0,
                       line_color="black"),
                  row=4,
                  col=1)
    # set 5th plot in the subplot
    fig.add_trace(go.Bar(x=df['Date'], y=df['Volume'], name="Volume"), 5, 1)
    # set 6th plot in the subplot - 籌碼分析 - 三大法人
    fig.add_trace(go.Bar(x=df['Date'], y=df['Foreign'], name="Foreign"), 6, 1)
    fig.add_trace(go.Bar(x=df['Date'], y=df['Trust'], name="Trust"), 6, 1)
    fig.add_trace(go.Bar(x=df['Date'], y=df['Dealer'], name="Dealer"), 6, 1)
    # set 7th plot in the subplot - 籌碼分析 - 外資持股比率
    maxNum, minNum = 0, 100
    for i in df['ForeignRatio']:
        if i > maxNum:
            maxNum = i
        elif i < minNum and i != 0:
            minNum = i
    fig.add_trace(go.Bar(x=df['Date'], y=df['ForeignRatio'], name="Chip"), 7,
                  1)
    fig.update_yaxes(range=[(minNum - 0.25), (maxNum + 0.25)], row=8, col=1)
    # set 9th plot in the subplot - 籌碼分析 - 股東持股分級週統計圖
    # fig.add_trace(go.Bar(x=df['Date'], y="股東持股分級", name="Chip"), 9, 1)
    # set the layout of the subplot
    fig.update_layout(
        title_text=showingName +
        "'s stock price visualization <a href='/score'> Visualize Stock Score </a>",
        height=1500,
        width=1500,
        legend=dict(orientation="h",
                    yanchor="bottom",
                    y=-0.15,
                    xanchor="right",
                    x=1),
        xaxis_rangeslider_visible=False,
        barmode='relative',
        hovermode='x')
    # remove empty from date list
    fig.update_xaxes(rangebreaks=[dict(values=dtBreaks)], showticklabels=False)
    ## end of fig
    return fig


def visualizePATH(fileBase, fileType='.csv'):
    fileList = []
    for dirPath, dirNames, fileNames in os.walk(fileBase):
        for i, f in enumerate(fileNames):
            if fileType in f:
                f_ = f.replace('.csv', '')
                fileList.append(f_)
    fileList.sort()
    # print(fileList)
    stockNameList = '../stockNumber/TW_all.txt'
    try:
        f = open(stockNameList, 'r', encoding='utf-8')
    except:
        print("No such file or directory : " + stockNameList + ".")
    tmpList = f.readlines()
    tmpList_ = []
    for tmp in tmpList:
        tmp_ = tmp.replace('\n', '')
        tmp_ = tmp_.split(' ')[0]
        tmpList_.append(tmp_)
    f.close()
    fileListwithName = []
    for fileList_ in fileList:
        name = ''
        stockNumber = fileList_.split('.')[0]
        for i in range(len(tmpList_)):
            if stockNumber == (tmpList_[i].split('\t')[0]):
                name = tmpList_[i].split('\t')[-1]
                break
        fileListwithName.append([fileList_, name])
    return fileListwithName



# Server Back End
import dash
# from dash import dcc, html
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import flask


# def visualizeStart(__name__, fileBase, fileName, length, dir=0):
fileBase = '../postData/'
timeLength = [45, 60, 90, 120, 240, 360, 480, 600]

# start app setting
app = flask.Flask(__name__)

dashapp = dash.Dash(
    __name__,
    server=app,
    title="Visualize Stock",
    url_base_pathname='/stock/',
    # routes_pathname_prefix='/stock/',
    # requests_pathname_prefix='/stock/'
)

fig_ = go.Figure()
dashapp.layout = html.Div([
    dcc.Dropdown(id='stock-list', options=[], value=0),
    dcc.Slider(
        id='time-length',
        min=timeLength[0],
        max=timeLength[-1],
        # default timeLength[2]: 90 days
        # -> 18 weeks, about 5 months
        # => 12 weeks, about 3 months, 1 quarter
        value=timeLength[2],
        marks={str(time_): str(time_)
               for time_ in timeLength},
        step=None),
    dcc.Graph(id="plot", figure=fig_, config={'displayModeBar': False})
])


@dashapp.callback(
    [Output('stock-list', 'options'),
     Output('stock-list', 'value')],
    [Input('stock-list', 'options'),
     Input('stock-list', 'value')])
def dropdownListRefresh(nowfileList, nowvalue):
    newfileList = visualizePATH(fileBase)
    newoptions_ = [{
        'label': str(name[1] + " " + name[0]),
        'value': str(name[0])
    } for name in newfileList]
    if len(nowfileList) == 0:
        return newoptions_, newoptions_[0]['value']
    return newoptions_, nowvalue


@dashapp.callback(
    Output('plot', 'figure'),
    [Input('stock-list', 'value'),
     Input('time-length', 'value')])
def graphCallback(fileName, length):
    if fileName == None:
        fileName = ''
    fig = graphFromFile(fileBase, fileName, length)
    return fig


@app.route('/score')
def scorepage():
    _pg_title = 'Visualize Stock Score'
    _pg_date = date.today()
    _pg_body = ''
    try:
        _pg_tables_data = pd.read_csv('../TotalScoreList.csv',
                                      dtype={'num_followers': np.int64})
    except:
        _pg_tables_data = ''  # fail to read file
    _pg_tables_data_1d = _pg_tables_data[_pg_tables_data["StockNumber"].str.contains(".1d") == True]
    _pg_tables_data_1wk = _pg_tables_data[_pg_tables_data["StockNumber"].str.contains(".1wk") == True]
    _pg_tables_data_1mo = _pg_tables_data[_pg_tables_data["StockNumber"].str.contains(".1mo") == True]
    _pg_tables = [_pg_tables_data_1d.to_html() + _pg_tables_data_1wk.to_html() + _pg_tables_data_1mo.to_html()]
    return flask.render_template('table.html',
                                 pg_title=_pg_title,
                                 pg_date=_pg_date,
                                 pg_body=_pg_body,
                                 pg_tables=_pg_tables)


def os_Caller():
    # os.system("@echo off")
    # os.seteuid(os.geteuid()) # does it work?
    # os.system("bash ../envSetup/datacrawler.sh --no-output") # fail on no wait
    import subprocess
    subprocess.Popen(["bash", "../envSetup/datacrawler.sh"]) # no wait
    return


@app.route('/refresh')
def refreshdata():
    try:
        return flask.render_template('refresh.html', pg_title='Refresh data')
    finally:
        os_Caller()
    return


@app.errorhandler(Exception)
def errorredir(e):
    return flask.render_template('redir.html', pg_title='redir...')


if __name__ == '__main__':
    print("Start flask without uwsgi, nginx, supervisor.")
    app.run()


