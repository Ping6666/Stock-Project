# version: 0.7

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from app_plotly import *


def create_dash(flask_app):
    fileBase = '../post_files/'
    timeLength = [45, 60, 90, 120, 240, 360, 480, 600, 1200]

    dashapp = Dash(
        __name__,
        server=flask_app,
        title="Visualize Stock",
        url_base_pathname='/stock/',
        # routes_pathname_prefix='/stock/',
        # requests_pathname_prefix='/stock/'
    )

    # figure
    fig_ = go.Figure()

    dashapp.layout = html.Div([
        dcc.Dropdown(id='stock-list', options=[], value=0),
        dcc.Slider(id='time-length',
                   min=timeLength[0],
                   max=timeLength[-1],
                   value=timeLength[2],
                   marks={str(time_): str(time_)
                          for time_ in timeLength},
                   step=None),
        dcc.Graph(id="plot", figure=fig_, config={'displayModeBar': False})
    ])

    # dcc.Dropdown
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

    # dcc.Slider
    @dashapp.callback(
        Output('plot', 'figure'),
        [Input('stock-list', 'value'),
         Input('time-length', 'value')])
    def graphCallback(fileName, length):
        if fileName == None:
            fileName = ''
        fig = create_graph(fileBase, fileName, length)
        return fig

    return dashapp
