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
            html.Div([
                html.H1('Kuznets demo', style={'display':'inline-block',}),
                html.A('Contact', href='mailto:alaistair@gmail.com',
                    style={'display':'inline-block',
                        'margin-top':'1em',
                        'float':'right',
                        'text-decoration':'none',
                        'padding-left':'1%',
                        'font-size':'0.8em'}),
                html.P('|',
                    style={'display':'inline-block',
                        'margin-top':'0.5em',
                        'float':'right',
                        'font-size':'1.1em'}),
                html.A('About', href='https://www.alaistairchan.com/kuznets.html',
                    style={'display':'inline-block',
                        'margin-top':'1em',
                        'float':'right',
                        'text-decoration':'none',
                        'padding-right':'1%',
                        'font-size':'0.8em'}),
            ],style={}),
            html.Hr(style={'margin-bottom':'3%'}),
            html.Div([
                html.Div([
                    html.H2('Simulation settings'),
                    html.P('Households: ' + str(len(self.economy.households))
                        + ' Firms: ' + str(len(self.economy.firms))),
                ], style={'display':'inline-block','width':'50%', }),
                html.Div([
                    html.H2('Policy settings'),
                    html.P('Interest rate (%)'),
                    dcc.Slider(
                        id='interest-rate',
                        min=0,
                        max=10,
                        step=0.25,
                        value=(self.economy.interest_rate-1)*100,
                        disabled=True,
                        marks={i:'{}'.format(i) for i in range(11)}
                    )
                ], style={'display':'inline-block', 'width':'50%', }),
                ], style={'margin-bottom':'5%', 'padding-left':'3%', 'padding-right':'3%'}),
            html.Div([
                html.P('Run simulation for ',
                    style={'display':'inline-block','vertical-align': 'middle', 'margin-right':'0.8%', 'padding-top':'2%'}),
                html.P(dcc.RadioItems(
                    id='cycle-update-box',
                    options=[
                        {'label': '1 ', 'value': '1'},
                        {'label': '5 ', 'value': '5'},
                        {'label': '20 ', 'value': '20'}
                    ],
                    value='5'),
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
            ], style={'padding-top':'0%','padding-left':'3%', 'padding-right':'3%'}),

            html.Div([
                dcc.Tabs(id='tabs',value='tab-1',children=[
                    dcc.Tab(label='Main graph',children=[
                        html.Div(dcc.Graph(id='main-graph',config={'displayModeBar': False},
                            style={'height':'45%','margin-top':'0%', 'padding-left':'3%', 'padding-right':'3%'})),
                        html.Div([
                            html.P('Households', style={'display':'inline-block', 'width':'25%'}),
                            html.P('Firms', style={'display':'inline-block', 'width':'25%'}),
                            html.P('Government', style={'display':'inline-block', 'width':'25%'}),
                            html.P('Macro', style={'display':'inline-block', 'width':'25%'}),
                        ], style={'font-size':'1.2em', 'padding-left':'10%', 'padding-right':'10%', 'margin-bottom':'-2%'}),
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
                                    {'label': 'Revenue', 'value': 'Firm revenue'},
                                    {'label': 'Debt', 'value': 'Firm debt'},
                                ],
                                values=[],
                                labelStyle={'display':'block'}),
                                style={'display':'inline-block','width':'25%','vertical-align':'top'}),
                            html.P(dcc.Checklist(
                                id='government-lines-checklist',
                                options=[
                                    {'label': 'Tax revenue', 'value': 'Government revenue'},
                                    {'label': 'Spending', 'value': 'Government expenditure'},
                                    {'label': 'Debt', 'value': 'Government debt'},
                                ],
                                values=[],
                                labelStyle={'display':'block'}),
                                style={'display':'inline-block','width':'25%','vertical-align':'top'}),
                            html.P(dcc.Checklist(
                                id='macro-lines-checklist',
                                options=[
                                    {'label': 'Inflation', 'value': 'CPI (R)'},
                                    {'label': 'Interest rate', 'value': 'Interest rate (R)'},
                                    {'label': 'Unemployment rate', 'value': 'Unemployment rate (R)'},
                                ],
                                values=[],
                                labelStyle={'display':'block'}),
                                style={'display':'inline-block','width':'25%','vertical-align':'top'}),
                        ], style={'padding-left':'10%', 'padding-right':'10%'}),
                    ]),
                    dcc.Tab(label='Looking deeper',children=[
                        html.Div(dcc.Dropdown(id='relationships-dropdown',
                            options=[
                                {'label': 'Okun\'s Law', 'value': 'Okun'},
                                {'label': 'Phillip\'s curve', 'value': 'Phillip'}], style={'width':'100%','float':'right'}),
                            style={'padding-left':'3%','padding-right':'3%','padding-top':'3%'}),
                        html.Div([
                            html.Div(id='relationships-text',
                                children=['init'],
                                style={'display':'inline-block','width':'40%','padding-top':'6%'}),
                            dcc.Graph(id='relationships-graph',config={'displayModeBar': False},
                                style={'display':'inline-block','width':'50%','height':'45%','margin-top':'0%','margin-right':'0%','float':'right'}),
                        ], style={'padding-left':'3%','padding-right':'3%','padding-top':'3%'})
                    ]),
                ]),
            ], style={'margin-top':'4%','padding-left':'3%', 'padding-right':'3%'}),

            html.Hr(style={'margin-top':'5%','margin-bottom':'-3%'}),
            html.Div([
                html.Div(
                    html.H5('© Alaistair Chan'),
                    className='copyright'),
            ], className='bottom'),

        ], style={'padding-left':'3%', 'padding-right':'3%'})

        @self.app.callback(
            [dash.dependencies.Output('main-graph', 'figure'),
            dash.dependencies.Output('loading-output-1', 'children'),
            dash.dependencies.Output('relationships-graph', 'figure')],
            [dash.dependencies.Input('household-lines-checklist', 'values'),
            dash.dependencies.Input('firm-lines-checklist', 'values'),
            dash.dependencies.Input('government-lines-checklist', 'values'),
            dash.dependencies.Input('macro-lines-checklist', 'values'),
            dash.dependencies.Input('cycle-update-button', 'n_clicks_timestamp'),
            dash.dependencies.Input('reset-button', 'n_clicks_timestamp'),
            dash.dependencies.Input('relationships-dropdown', 'value')],
            [dash.dependencies.State('cycle-update-box', 'value'),
            dash.dependencies.State('interest-rate', 'value')
            ])
        def update_main_graph(household_lines_checklist, firm_lines_checklist,
            government_lines_checklist, macro_lines_checklist,
            n_clicks_timestamp_1, n_clicks_timestamp_2, relationships_dropdown, value_1, value_2):


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
                            )},'',{
                        'data':[],
                        'layout':
                            go.Layout(
                                xaxis={'title':''},
                                yaxis={'title':''},
                            )}]

            main_graph_data = []
            relationships_graph_data = []
            relationships_graph_layout = []

            for i in household_lines_checklist:
                if i == 'Household income':
                    main_graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_production_cycle_data()[i],
                        name = i,
                        line = {'color':'rgb(255,255,0)'},
                        legendgroup = 'Households',
                    ))
                elif i == 'Household spending':
                    main_graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_consumption_cycle_data()[i],
                        name = i,
                        line = {'color':'rgb(255,140,0)'},
                        legendgroup = 'Households',
                    ))
                elif i == 'Household savings':
                    main_graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_financial_cycle_data()[i],
                        name = i,
                        line = {'color':'rgb(128,0,0)'},
                        legendgroup = 'Households',
                    ))
            for i in firm_lines_checklist:
                if i == 'Firm inventory':
                    main_graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_production_cycle_data()[i],
                        name = i,
                        line = {'color':'rgb(100,149,237)'},
                        legendgroup = 'Firms',
                    ))
                elif i == 'Firm revenue':
                    main_graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_consumption_cycle_data()[i],
                        name = i,
                        line = {'color':'rgb(128,0,128)'},
                        legendgroup = 'Firms',

                    ))
                elif i == 'Firm debt':
                    main_graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_financial_cycle_data()[i],
                        name = i,
                        line = {'color':'rgb(25,25,112)'},
                        legendgroup = 'Firms',
                    ))
            for i in government_lines_checklist:
                if i == 'Government revenue':
                    main_graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_consumption_cycle_data()[i],
                        name = i,
                        line = {'color':'rgb(0,100,0)'},
                        legendgroup = 'Government',
                    ))
                elif i == 'Government expenditure':
                    main_graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_consumption_cycle_data()[i],
                        name = i,
                        line = {'color':'rgb(124,252,0)'},
                        legendgroup = 'Government',
                    ))
                elif i == 'Government debt':
                    main_graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_consumption_cycle_data()[i],
                        name = i,
                        line = {'color':'rgb(152,251,152)'},
                        legendgroup = 'Government',
                    ))
            for i in macro_lines_checklist:
                if i == 'CPI (R)':
                    main_graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_consumption_cycle_data()['CPI'],
                        name = i,
                        line = {},
                        yaxis = 'y2',
                        legendgroup = 'Macro',
                    ))
                elif i == 'Interest rate (R)':
                    main_graph_data.append(go.Scatter(
                        x = self.index,
                        y = (self.economy.get_consumption_cycle_data()['Interest rate']-1)*100,
                        name = i,
                        yaxis = 'y2',
                        legendgroup = 'Macro',
                    ))
                elif i == 'Unemployment rate (R)':
                    main_graph_data.append(go.Scatter(
                        x = self.index,
                        y = self.economy.get_consumption_cycle_data()['Unemployment rate']*100,
                        name = i,
                        yaxis = 'y2',
                        legendgroup = 'Macro',
                    ))
            if relationships_dropdown == 'Okun':
                relationships_graph_data.append(go.Scatter(
                    x = self.economy.get_consumption_cycle_data()['Unemployment rate'].diff()*100,
                    y = self.economy.get_production_cycle_data()['Firm production'].pct_change()*100,
                    name = 'Okun',
                    mode='markers'
                ))
                relationships_graph_layout = go.Layout(
                    xaxis={'title':'Change in unemployment rate'},
                    yaxis={'title':'Change in GDP growth'},
                )
            elif relationships_dropdown == 'Phillip':
                relationships_graph_data.append(go.Scatter(
                    x = self.economy.get_consumption_cycle_data()['CPI'].pct_change()*100,
                    y = self.economy.get_production_cycle_data()['Unemployment rate']*100,
                    name = 'Phillip',
                    mode='markers'
                ))
                relationships_graph_layout = go.Layout(
                    xaxis={'title':'Inflation rate'},
                    yaxis={'title':'Unemployment rate'},
                )
            else:
                relationships_graph_data.append(go.Scatter(
                    x = [0],
                    y = [0],
                    name = '',
                    mode='markers'
                ))
                relationships_graph_layout = go.Layout(
                    xaxis={'title':''},
                    yaxis={'title':''},
                )

            return [{
                'data':main_graph_data, # main graph
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
                    )},'',{
                'data':relationships_graph_data, # relationships graph
                'layout':relationships_graph_layout
                }]

        @self.app.callback(
            dash.dependencies.Output('relationships-text', 'children'),
            [dash.dependencies.Input('relationships-dropdown', 'value')])
        def relationships_text(value_1):
            if value_1 == 'Okun':
                return(dcc.Markdown('''**Okun\'s law** describes a relationship between **unemployment** and **GDP growth**.
                    Arthur Okun in 1962 found that when GDP growth increases by 2%, the unemployment rate falls by 1%.
                    Although those numbers work for the U.S., the negative relationship between changes in unemployment and GDP
                    growth can be seen everywhere.
                    '''))
            elif value_1 == 'Phillip':
                return(dcc.Markdown('''When William Phillips graphed inflation and unemployment for the UK economy in 1958 he found
                    an inverse relationship between the two. The **Phillips curve** shows that **lower unemployment** generally leads to **higher
                    inflation**, and vice versa. Over the years, and especially in the 1970s, this relationship began to break down. It
                    was found that the Phillips curve only worked in the short run, and that monetary factors drove inflation in the
                    longer term.'''))
            else:
                return(dcc.Markdown('''Choose an economic relationship from the dropdown menu above to see it recreated by the Kuznets simulation.'''))
