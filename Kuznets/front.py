import sys

from settings import Settings
from economy import Economy
import numpy as np
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

external_stylesheets = ['./style.css']

class App():
    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        self.settings = Settings()
        self.economy = Economy(self.settings)

        for i in range(20):
            self.economy.cycle()


        self.index = self.economy.economy_data.index.get_level_values(0).unique()
        self.graph_economy(self.economy)

    def graph_economy(self, economy):
        self.app.layout = html.Div(children=[
            html.H1(children='Kuznets'),
            dcc.Graph(id='economy',config={'displayModeBar': False}),
            dcc.Checklist(
                id='checklist',
                options=[
                    {'label': 'Total household income', 'value': 'hh income'},
                    {'label': 'Total household savings', 'value': 'hh savings'},
                    {'label': 'Total household spending', 'value': 'hh spending'},
                    {'label': 'CPI', 'value': 'CPI'},
                    {'label': 'Total firm inventory', 'value': 'firm inventory'},
                    {'label': 'Total firm production', 'value': 'firm production'},
                    {'label': 'Total firm revenue', 'value': 'firm revenue'},
                    {'label': 'Total firm debt', 'value': 'firm debt'},
                ],
                values=['hh savings', 'hh spending']
            ),
        ])

        @self.app.callback(
            dash.dependencies.Output('economy', 'figure'),
            [dash.dependencies.Input('checklist', 'values')]
        )
        def update_graph(graphs):
            graph_data = []
            print('test')

            for i in graphs:
                if i == 'hh income' or i == 'firm production' or i == 'firm inventory':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_production_cycle_data()[i],
                        name = i
                    ))
                elif i == 'hh spending' or i == 'firm revenue':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_consumption_cycle_data()[i],
                        name = i
                    ))
                elif i == 'hh savings' or i == 'firm debt':
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

            return {
                'data':graph_data,
                'layout':
                    go.Layout(
                        xaxis={'title':'Year'},
                        yaxis={'title':'$'},
                        yaxis2={'title':'Index',
                                'overlaying':'y',
                                'side':'right'}
                    )
            }
