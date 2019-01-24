import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
hh_income = {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'income'}

app.layout = html.Div(children=[
    html.H1(children='EconSim'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='Households',
        figure={
            'data': [
                hh_income,
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Households'
            }
        }
    ),
    dcc.Graph(
        id='Firms',
        figure={
            'data': [
                income,
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Firms'
            }
        }
    )
])

def hh_income():
    return 1#hh_income = {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'income'}


def graph_data():
    print('e')
