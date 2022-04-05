from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from server import app
from views.time import time_view
# from views.demo import demo_view

# styling options
card_style = {
    "padding": "2rem 2rem",
}

# page header
card_page_header = dbc.Card([
    html.H1('COVID-19 Case Surveillance Data Warehouse'),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dbc.Label('Database source'),
            dcc.Dropdown(
                id='main-data-source',
                options=[
                    {'label':'MySQL','value':1},
                    {'label':'MongoDB','value':2},
                    {'label':'Neo4J','value':3},
                ],value=1 # default to MySQL
            )
        ]),
        dbc.Col([
            dbc.Label('Plot view'),
            dcc.Dropdown(
                id='main-plot-view',
                options=[
                    {'label':'Time-Location','value':'time'},
                    {'label':'Demography','value':'demo'},
                ], value=1 # default to time-location dimension
            )
        ])
    ])
], style = card_style )

# app layout - use cards
app.layout = dbc.Container([
    card_page_header,
    html.Div(
        id='content',
        style={
            'flex':'auto'
        }
    )
    # app_view_1.card_time_series,
    # app_view_1.card_map
])

# callback control for viewing content
@app.callback(
    Output('content','children'),
    Input('main-plot-view','value')
    )
def render_content(value):
    if value == 'time':
        return time_view
    # elif value == 'demo':
    #     return demo_view

if __name__ == '__main__':
    app.run_server()