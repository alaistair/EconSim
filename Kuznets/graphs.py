import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

external_stylesheets = ['static/style.css']

class Bar_graph():
    def __init__(self, economy):
        self.app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        self.economy = economy
        self.index = self.economy.economy_data.get_level_values(0).unique()
        self.graph_economy(economy)

    def graph_economy(self, economy):
        self.app.layout = html.Div(children=[
            html.H1(children='EconSim'),
            html.Label('Display options'),
            dcc.Graph(id='economy',config={'displayModeBar': False}),
            dcc.Checklist(
                id='checklist',
                options=[
                    {'label': 'Total household income', 'value': 'total hh income'},
                    {'label': 'Total household savings', 'value': 'total hh savings'},
                    {'label': 'Total household spending', 'value': 'total hh spending'},
                    {'label': 'Total firm inventory', 'value': 'total firm inventory'},
                    {'label': 'Total firm production', 'value': 'total firm production'},
                    {'label': 'Total firm revenue', 'value': 'total firm revenue'},
                    {'label': 'Total firm debt', 'value': 'total firm debt'},
                ],
                values=['total hh savings', 'total hh spending']
            ),
        ])

        @self.app.callback(
            dash.dependencies.Output('economy', 'figure'),
            [dash.dependencies.Input('checklist', 'values')]
        )
        def update_graph(graphs):
            graph_data = []
            for i in graphs:
                if i == 'total hh income' or i == 'total firm production' or i == 'total firm inventory':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_production_cycle_data()[i],
                        name = i
                    ))
                elif i == 'total hh spending' or i == 'total firm revenue':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_consumption_cycle_data()[i],
                        name = i
                    ))
                elif i == 'total hh savings' or i == 'total firm debt':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_financial_cycle_data()[i],
                        name = i
                    ))

            return {
                'data':graph_data,
                'layout':
                    go.Layout(
                        xaxis={'title':'Year'},
                        yaxis={'title':'$'}
                    )
            }
