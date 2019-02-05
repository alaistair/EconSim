import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets = ['https://alaistairchan.com/objects/style.css']

class Bar_graph():
    def __init__(self, households_data, firms_data):
        self.app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        self.app.layout = html.Div(children=[
            html.H1(children='EconSim'),
            #html.Div([
            dcc.Graph(
                id='households',
            ),
            dcc.Slider(
                id='households-year-slider',
                min=0,
                max=households_data.index.get_level_values('time').max(),
                value=households_data.index.get_level_values('time').max(),
                marks={str(time): str(time) for time in households_data.index.get_level_values('time').unique()}
            ),
            dcc.Graph(
                id='firms',
            ),
            dcc.Slider(
                id='firms-year-slider',
                min=0,
                max=firms_data.index.get_level_values('time').max(),
                value=firms_data.index.get_level_values('time').max(),
                marks={str(time): str(time) for time in firms_data.index.get_level_values('time').unique()}
            )
        #])
        ])

        @self.app.callback(
            dash.dependencies.Output('households', 'figure'),
            [dash.dependencies.Input('households-year-slider', 'value')])

        def update_figure(selected_year):
            bars = ['income', 'savings', 'spending']
            traces = []
            for bar in bars:
                traces.append(go.Bar(
                    x = households_data.index.get_level_values('hhID').unique(),
                    y = households_data[bar][selected_year],
                    name = bar,
                ))

            return {
                'data': traces,
                'layout': go.Layout(
                    {'title':'Households'},
                    #xaxis={'title':'number'},
                    yaxis={'title':'$'},
                    legend={'x': 0, 'y': 1},

                    #margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                )}

        @self.app.callback(
            dash.dependencies.Output('firms', 'figure'),
            [dash.dependencies.Input('firms-year-slider', 'value')])

        def update_figure(selected_year):
            bars = ['inventory', 'production', 'revenue']
            traces = []
            for bar in bars:
                traces.append(go.Bar(
                    x = [1,2,3,4,5,6,7,8,9,10],
                    y = firms_data[bar][selected_year],
                    name = bar,
                ))

            return {
                'data': traces,
                'layout': go.Layout(
                    {'title':'Firms'},
                    #xaxis={'title':'number'},
                    yaxis={'title':'$'},
                    legend={'x': 0, 'y': 1},

                    #margin={'l': 40, 'b': 40, 't': 10, 'r': 10},

                )}
