# version: 1.0

import os
import pandas as pd

pd.options.display.float_format = '{:.3f}'.format

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def file_read(fileBase, fileName):
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
    return (df, showingName)


def file_cht_name(showingName):
    # take out the chinese name of cc = TW stock
    stockNameList = "./stock_number/TW_all.txt"
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
        target_stock_no = showingName.split('.')[0]
        for i in range(len(tmpList_)):
            if target_stock_no == (tmpList_[i].split('\t')[0]):
                showingName = tmpList_[i].split('\t')[-1] + " " + showingName
                break
    return showingName


def subgraph_1(df, fig):
    # Stock Price
    fig.add_trace(
        go.Candlestick(x=df['Date'],
                       open=df['Open'],
                       high=df['High'],
                       low=df['Low'],
                       close=df['Close'],
                       name="Candlestick"), 1, 1)
    # Keltner Channel
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
    # MA
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
    return fig


def subgraph_2(df, df_, fig, timeLength, checkLen):
    # Score
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Score'], name="Score"), 2, 1)
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['Score_SMA_5'], name="Score SMA-5"), 2,
        1)
    # fig.add_trace(
    #     go.Scatter(x=df['Date'], y=df['ScorePoint'], name="ScorePoint"), 2, 1)
    fig.add_shape(dict(type="line",
                       x0=0,
                       x1=timeLength,
                       y0=-30,
                       y1=-30,
                       line_color="black"),
                  row=2,
                  col=1)
    fig.add_shape(dict(type="line",
                       x0=0,
                       x1=timeLength,
                       y0=0,
                       y1=0,
                       line_color="black"),
                  row=2,
                  col=1)
    fig.add_shape(dict(type="line",
                       x0=0,
                       x1=timeLength,
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
    return fig


def subgraph_3(df, fig, timeLength):
    # KD * KSI
    fig.add_trace(go.Scatter(x=df['Date'], y=df['K'], name="K*RSI"), 3, 1)
    fig.add_trace(go.Scatter(x=df['Date'], y=df['D'], name="D*RSI"), 3, 1)
    fig.add_shape(dict(type="line",
                       x0=0,
                       x1=timeLength,
                       y0=10,
                       y1=10,
                       line_color="black"),
                  row=3,
                  col=1)
    fig.add_shape(dict(type="line",
                       x0=0,
                       x1=timeLength,
                       y0=70,
                       y1=70,
                       line_color="black"),
                  row=3,
                  col=1)
    return fig


def subgraph_4(df, fig, timeLength):
    # Ichimoku Clouds
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
                       x1=timeLength,
                       y0=0,
                       y1=0,
                       line_color="black"),
                  row=4,
                  col=1)
    return fig


def subgraph_5(df, fig):
    # Volume
    fig.add_trace(go.Bar(x=df['Date'], y=df['Volume'], name="Volume"), 5, 1)
    return fig


def subgraph_6(df, fig):
    # 籌碼分析 - 三大法人
    fig.add_trace(go.Bar(x=df['Date'], y=df['Foreign'], name="Foreign"), 6, 1)
    fig.add_trace(go.Bar(x=df['Date'], y=df['Trust'], name="Trust"), 6, 1)
    fig.add_trace(go.Bar(x=df['Date'], y=df['Dealer'], name="Dealer"), 6, 1)
    return fig


def subgraph_7(df, fig):
    # 籌碼分析 - 外資持股比率
    maxNum, minNum = 0, 100
    for i in df['ForeignRatio']:
        if i > maxNum:
            maxNum = i
        elif i < minNum and i != 0:
            minNum = i
    fig.add_trace(go.Bar(x=df['Date'], y=df['ForeignRatio'], name="Chip"), 7,
                  1)
    fig.update_yaxes(range=[(minNum - 0.25), (maxNum + 0.25)], row=7, col=1)
    return fig


def create_graph(fileBase, fileName, timeLength_):
    df, showingName = file_read(fileBase, fileName)
    showingName = file_cht_name(showingName)
    timeLength_ = min(timeLength_, len(df))  # max time len

    # for check volume low point
    checkLen = 60
    timeLengthTmp = min(timeLength_ + checkLen + 1, len(df))
    df_ = df[-timeLengthTmp:]
    # end

    # remove empty date
    df = df[-timeLength_:]
    dtAll = pd.date_range(start=df['Date'].iloc[0], end=df['Date'].iloc[-1])
    dtAll = dtAll.strftime("%Y/%m/%d")
    dtBreaks = [d for d in dtAll if d not in df['Date'].tolist()]
    # end

    # csv : Date, Open, High, Low, Close, Volume, KC, KD * RSI, 外資, 投信, 自營商, 外資持股比率, 股東持股分級

    # set the graph be subplot type
    fig = make_subplots(
        rows=7,
        cols=1,
        row_heights=[0.4, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
        vertical_spacing=0.05,
        shared_xaxes=True,
        subplot_titles=("Candlestick Charts", "Score (high: buy, low: sell)",
                        "KD*RSI", "Ichimoku Indicator", "Volume",
                        "Chip Analysis", "Foreign Chip Ratio"))

    # add subgraphs
    fig = subgraph_1(df, fig)
    fig = subgraph_2(df, df_, fig, timeLength_, checkLen)
    fig = subgraph_3(df, fig, timeLength_)
    fig = subgraph_4(df, fig, timeLength_)
    fig = subgraph_5(df, fig)
    fig = subgraph_6(df, fig)
    fig = subgraph_7(df, fig)

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
    stockNameList = "./stock_number/TW_all.txt"
    try:
        f = open(stockNameList, 'r', encoding='utf-8')
    except:
        print("No such file or directory : " + stockNameList + ".")
        return []  # None
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
        target_stock_no = fileList_.split('.')[0]
        for i in range(len(tmpList_)):
            if target_stock_no == (tmpList_[i].split('\t')[0]):
                name = tmpList_[i].split('\t')[-1]
                break
        fileListwithName.append([fileList_, name])
    return fileListwithName
