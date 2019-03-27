import sys
import time

from src.economy import Economy
from src.settings import Settings
import numpy as np
import pandas as pd

import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

class App():
    def __init__(self):

        self.server = flask.Flask(__name__)
        self.app = dash.Dash(__name__, server=self.server)
        self.app.title = 'Kuznets'

        self.last_cycle_click = 0 # used for cycle check
        self.last_reset_click = 0 # used for reset check
        self.settings = Settings()
        self.economy = Economy(self.settings)

        self.index = self.economy.economy_data.index.get_level_values(0).unique()

        self.app.layout = html.Div(children=[
            html.H1(['Kuznets demo ', html.A('Link', href='www.alaistairchan.com')]),
            html.A('About', href='https://www.alaistairchan.com/kuznets/about.html'),

            html.Div([
                html.H2('Simulation settings'),
                html.P('Households: ' + str(self.last_cycle_click)
                    + ' Firms: ' + str(self.last_cycle_click)),
            ]),
            html.Div([
                html.H2('Policy settings'),
                html.P('Interest rate (%)'),
                dcc.Slider(
                    id='interest-rate',
                    min=0,
                    max=10,
                    step=0.25,
                    value=(self.economy.interest_rate-1)*100,
                    marks={i:'{}'.format(i) for i in range(11)}
                )
            ], style={'width':'30%', 'margin-bottom':'5%'}),
            html.Div([
                html.P('Run simulation for ',
                    style={'display':'inline-block','vertical-align': 'middle', 'margin-right':'0.8%', 'padding-top':'2%'}),
                html.P(dcc.RadioItems(
                    id='cycle-update-box',
                    options=[
                        {'label': '1 ', 'value': '1'},
                        {'label': '10 ', 'value': '10'},
                        {'label': '50 ', 'value': '50'}
                    ],
                    value='10'),
                    style={'display':'inline-block','vertical-align': 'middle', 'padding-top':'2%'}),
                html.P('cycles ',
                    style={'display':'inline-block','vertical-align': 'middle', 'margin-left':'0.8%','margin-right':'2%', 'padding-top':'2%'}),
                html.Div(html.Button(
                    'Run',
                    id='cycle-update-button',
                    n_clicks=0,
                    value = '0'),
                    style={'width':'10%', 'display':'inline-block','vertical-align': 'middle', 'padding-top':'2%'}),
                html.Div(html.Button(
                    'reset',
                    id='reset-button',
                    n_clicks=0),
                    style={'width':'10%', 'display':'inline-block','vertical-align': 'middle', 'padding-top':'2%'}),
                html.Div(dcc.Loading(
                    id='loading-1',
                    children=[html.Div(id='loading-output-1')],
                    type='dot',),
                    style={'width':'10%', 'display':'inline-block','vertical-align': 'middle', 'height':'1%'})
            ], style={'padding-top':'0%'}),

            html.Div(dcc.Graph(id='economy',config={'displayModeBar': False},
                style={'height':'45%','margin-top':'0%'})),

            html.Div([
                html.P('Households', style={'display':'inline-block', 'width':'25%'}),
                html.P('Firms', style={'display':'inline-block', 'width':'25%'}),
                html.P('Government', style={'display':'inline-block', 'width':'25%'}),
                html.P('Macro', style={'display':'inline-block', 'width':'25%'}),
            ], style={'font-size':'1.2em', 'margin-bottom':'-3%'}),
            html.Div([
                html.P(dcc.Checklist(
                    id='household-lines-checklist',
                    options=[
                        {'label': 'Income', 'value': 'Household income'},
                        {'label': 'Savings', 'value': 'Household savings'},
                        {'label': 'Spending', 'value': 'Household spending'},
                    ],
                    values=['Household savings', 'Household spending'],
                    labelStyle={'display':'block'}),
                    style={'display':'inline-block','width':'25%','vertical-align':'top'}),
                html.P(dcc.Checklist(
                    id='firm-lines-checklist',
                    options=[
                        {'label': 'Inventory', 'value': 'Firm inventory'},
                        {'label': 'Production', 'value': 'Firm production'},
                        {'label': 'Revenue', 'value': 'Firm revenue'},
                        {'label': 'Debt', 'value': 'Firm debt'},
                    ],
                    values=[],
                    labelStyle={'display':'block'}),
                    style={'display':'inline-block','width':'25%','vertical-align':'top'}),
                html.P(dcc.Checklist(
                    id='government-lines-checklist',
                    options=[
                        {'label': 'Revenue', 'value': 'Government revenue'},
                        {'label': 'Spending', 'value': 'Government expenditure'},
                        {'label': 'Debt', 'value': 'Government debt'},
                    ],
                    values=[],
                    labelStyle={'display':'block'}),
                    style={'display':'inline-block','width':'25%','vertical-align':'top'}),
                html.P(dcc.Checklist(
                    id='macro-lines-checklist',
                    options=[
                        {'label': 'CPI', 'value': 'CPI (R)'},
                        {'label': 'Interest rate', 'value': 'Interest rate (R)'},
                        {'label': 'Unemployment rate', 'value': 'Unemployment rate (R)'},
                    ],
                    values=[],
                    labelStyle={'display':'block'}),
                    style={'display':'inline-block','width':'25%','vertical-align':'top'}),
            ]),
            html.Div([
                html.H2('Looking deeper'),
                html.P('Interest rate')
            ]),
            html.Table(

            ),
        ], style={'padding-left':'5%', 'padding-right':'5%'})

        @self.app.callback(
            [dash.dependencies.Output('economy', 'figure'),
            dash.dependencies.Output('loading-output-1', 'children')],
            [dash.dependencies.Input('household-lines-checklist', 'values'),
            dash.dependencies.Input('firm-lines-checklist', 'values'),
            dash.dependencies.Input('government-lines-checklist', 'values'),
            dash.dependencies.Input('macro-lines-checklist', 'values'),
            dash.dependencies.Input('cycle-update-button', 'n_clicks_timestamp'),
            dash.dependencies.Input('reset-button', 'n_clicks_timestamp')],
            [dash.dependencies.State('cycle-update-box', 'value'),
            dash.dependencies.State('interest-rate', 'value')
            ])
        def update_graph(household_lines_checklist, firm_lines_checklist,
            government_lines_checklist, macro_lines_checklist,
            n_clicks_timestamp_1, n_clicks_timestamp_2, value_1, value_2):

            if n_clicks_timestamp_1 is not None: # run simulation
                if n_clicks_timestamp_1 > self.last_cycle_click: # update cycle
                    self.economy.interest_rate = 1 + value_2/100
                    self.economy.cycle(int(value_1))
                    self.index = self.economy.economy_data.index.get_level_values(0).unique()
                    self.last_cycle_click = n_clicks_timestamp_1

            if n_clicks_timestamp_2 is not None: # reset simulation
                if n_clicks_timestamp_2 > self.last_reset_click:
                    self.settings = Settings()
                    self.economy = Economy(self.settings)

                    self.index = self.economy.economy_data.index.get_level_values(0).unique()
                    self.last_reset_click = n_clicks_timestamp_2
                    return [{
                        'data':[],
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

            graph_data = []

            for i in household_lines_checklist:
                if i == 'Household income':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_production_cycle_data()[i],
                        name = i,
                        line = {'color':'rgb(128,0,0)'},
                        legendgroup = 'Households',
                    ))
                elif i == 'Household spending':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_consumption_cycle_data()[i],
                        name = i,
                        line = {'color':'rgb(255,140,0)'},
                        legendgroup = 'Households',
                    ))
                elif i == 'Household savings':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_financial_cycle_data()[i],
                        name = i,
                        line = {'color':'rgb(255,255,0)'},
                        legendgroup = 'Households',
                    ))
            for i in firm_lines_checklist:
                if i == 'Firm production':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_production_cycle_data()[i],
                        name = i,
                        line = {'color':'rgb(0,255,255)'},
                        legendgroup = 'Firms',
                    ))
                elif i == 'Firm inventory':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_production_cycle_data()[i],
                        name = i,
                        line = {'color':'rgb(100,149,237)'},
                        legendgroup = 'Firms',
                    ))
                elif i == 'Firm revenue':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_consumption_cycle_data()[i],
                        name = i,
                        line = {'color':'rgb(128,0,128)'},
                        legendgroup = 'Firms',

                    ))
                elif i == 'Firm debt':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_financial_cycle_data()[i],
                        name = i,
                        line = {'color':'rgb(25,25,112)'},
                        legendgroup = 'Firms',
                    ))
            for i in government_lines_checklist:
                if i == 'Government revenue':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_consumption_cycle_data()[i],
                        name = i,
                        line = {'color':'rgb(0,100,0)'},
                        legendgroup = 'Government',

                    ))
                elif i == 'Government expenditure':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_consumption_cycle_data()[i],
                        name = i,
                        line = {'color':'rgb(124,252,0)'},
                        legendgroup = 'Government',
                    ))
                elif i == 'Government debt':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_consumption_cycle_data()[i],
                        name = i,
                        line = {'color':'rgb(152,251,152)'},
                        legendgroup = 'Government',
                    ))
            for i in macro_lines_checklist:
                if i == 'CPI (R)':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_consumption_cycle_data()['CPI'],
                        name = i,
                        yaxis = 'y2',
                        legendgroup = 'Macro',
                    ))
                elif i == 'Interest rate (R)':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = (self.economy.get_consumption_cycle_data()['Interest rate']-1)*100,
                        name = i,
                        yaxis = 'y2',
                        legendgroup = 'Macro',
                    ))
                elif i == 'Unemployment rate (R)':
                    graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_consumption_cycle_data()['Unemployment rate']*100,
                        name = i,
                        yaxis = 'y2',
                        legendgroup = 'Macro',
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
                            'showgrid':False,
                            'automargin':True,
                        },
                        legend={'orientation':'h',
                            'y':-0.3},
                        autosize=True

                    )
            },'']
