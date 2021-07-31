# take out data from csv file and then visualize the data
import pandas as pd
from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

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
    timeLength_ = min(timeLength_, len(df))
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
        subplot_titles=("Candlestick Charts", "Score (high: buy, low: sell)",
                        "KD*RSI", "Ichimoku Indicator", "Volume",
                        "Chip Aanalysis", "Foreign Chip Ratio"))
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
                   name="KeltnerChannel-H",
                   visible='legendonly'), 1, 1)
    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df['KC_middle'],
                   name="KeltnerChannel-M",
                   visible='legendonly'), 1, 1)
    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df['KC_low'],
                   name="KeltnerChannel-L",
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
    # set 3rd plot in the subplot - KD*KSI
    fig.add_trace(go.Scatter(x=df['Date'], y=df['K'], name="Stoch-K*RSI"), 3,
                  1)
    fig.add_trace(go.Scatter(x=df['Date'], y=df['D'], name="Stoch-D*RSI"), 3,
                  1)
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
        go.Scatter(x=df['Date'],
                   y=df['ICH_plot_1'],
                   name="ICH - Rise Potential"), 4, 1)
    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df['ICH_plot_2'],
                   name="ICH - Cloud Protection"), 4, 1)
    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=df['ICH_plot_3'],
                   name="ICH - Cloud Distance"), 4, 1)
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
    fig.update_yaxes(range=[(minNum - 0.25), (maxNum + 0.25)], row=7, col=1)
    # set 8th plot in the subplot - 籌碼分析 - 股東持股分級週統計圖
    # fig.add_trace(go.Bar(x=df['Date'], y="股東持股分級", name="Chip"), 8, 1)
    # set the layout of the subplot
    fig.update_layout(title_text=showingName + "'s stock price visualization",
                      height=1200,
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


def visualizeStart(fileBase, fileName, length):
    # start app setting
    app = dash.Dash(__name__)
    fig_ = graphFromFile(fileBase, fileName, length)
    app.layout = html.Div(
        [dcc.Graph(figure=fig_, config={'displayModeBar': False})])
    # For Development only, otherwise use gunicorn or uwsgi to launch, e.g.
    # gunicorn -b 0.0.0.0:8050 index:app.server
    app.run_server(port=8080, host='127.0.0.1', debug=False)
    return
