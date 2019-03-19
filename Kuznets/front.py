import sys
import time

from economy import Economy
from settings import Settings
import numpy as np
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['/static/style.css']

class App():
    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        self.app.title = 'Kuznets'
        self.cycle_clicks = 0 # used for button
        self.settings = Settings()
        self.economy = Economy(self.settings)

        self.index = self.economy.economy_data.index.get_level_values(0).unique()

        self.app.layout = html.Div(children=[
            html.H1(children='Kuznets'),

            html.Div([
                html.H2('Policy settings'),
                html.P('Interest rate')
            ]),
            html.Div([
                html.P('Run simulation for ',
                    style={'display':'inline-block','vertical-align': 'middle', 'padding-right':'0.8%'}),
                html.Div(dcc.Dropdown(
                    options=[
                        {'label': '1', 'value': '1'},
                        {'label': '10', 'value': '10'},
                        {'label': '50', 'value': '50'}
                    ],
                    value='10', id='cycle-input-box'),
                    style={'width':'8%', 'display':'inline-block','vertical-align': 'middle'}),
                html.P('cycles ',
                    style={'display':'inline-block','vertical-align': 'middle', 'padding-left':'0.8%'}),
                html.Div(html.Button(
                    'Run',
                    id='cycle-update-button',
                    n_clicks=0,
                    value = '0'),
                    style={'width':'20%', 'display':'inline-block','vertical-align': 'middle', 'padding':'4%'}),
                html.Div(dcc.Loading(
                    id='loading-1',
                    children=[html.Div(id='loading-output-1')],
                    type='dot'),
                    style={'width':'10%', 'display':'inline-block','vertical-align': 'middle'})
            ], style={}),

            html.Div(dcc.Graph(id='economy',config={'displayModeBar': False})),
            html.Div([html.H2('Display settings'),
                dcc.Checklist(
                    id='checklist',
                    options=[
                        {'label': 'Total household income', 'value': 'Household income'},
                        {'label': 'Total household savings', 'value': 'Household savings'},
                        {'label': 'Total household spending', 'value': 'Household spending'},
                        {'label': 'CPI', 'value': 'CPI'},
                        {'label': 'Total firm inventory', 'value': 'firm inventory'},
                        {'label': 'Total firm production', 'value': 'firm production'},
                        {'label': 'Total firm revenue', 'value': 'firm revenue'},
                        {'label': 'Total firm debt', 'value': 'firm debt'},
                    ],
                    values=['Household savings', 'Household spending'])])
        ])

        @self.app.callback(
            [dash.dependencies.Output('economy', 'figure'),
            dash.dependencies.Output('loading-output-1', 'children')],
            [dash.dependencies.Input('checklist', 'values'),
            dash.dependencies.Input('cycle-update-button', 'n_clicks')],
            [dash.dependencies.State('cycle-input-box', 'value')])
        def update_graph(graphs, n_clicks, value):
            if n_clicks > self.cycle_clicks: # update cycle
                self.economy.cycle(int(value))
                self.index = self.economy.economy_data.index.get_level_values(0).unique()
                self.cycle_clicks += 1

            graph_data = []

            for i in graphs:
                if i == 'Household income':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_production_cycle_data()['hh income'],
                        name = i
                    ))
                elif i == 'Household spending':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_consumption_cycle_data()['hh spending'],
                        name = i
                    ))
                elif i == 'Household savings':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_financial_cycle_data()['hh savings'],
                        name = i
                    ))
                elif i == 'firm production' or i == 'firm inventory':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_production_cycle_data()[i],
                        name = i
                    ))
                elif i == 'firm revenue':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_consumption_cycle_data()[i],
                        name = i
                    ))
                elif i == 'firm debt':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_financial_cycle_data()[i],
                        name = i
                    ))
                elif i == 'CPI':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_consumption_cycle_data()[i],
                        name = i,
                        yaxis = 'y2'
                    ))
            return [{
                'data':graph_data,
                'layout':
                    go.Layout(
                        xaxis={'title':'Year'},
                        yaxis={'title':'$'},
                        yaxis2={'title':'Index',
                                'overlaying':'y',
                                'side':'right',
                                'showgrid':False}
                    )
            },'']
