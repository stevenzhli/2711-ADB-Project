from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_extensions.enrich import Output, Input, State, ServersideOutput
from server import app
from model.mongo import get_mongo_data
from model.mysql import get_mysql_data
from model.neo4j import get_neo4j_data
from views.time import time_view
from views.demogr import demogr_view

# styling options
card_style = {
    'padding': '1rem 2rem',
}

# page header
card_page_header = dbc.Card([
    html.H2('COVID-19 Case Surveillance Data Warehouse'),
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
                ],value=None # default to MySQL
            ),
            dcc.Loading(dcc.Store(id='store-df_s'), fullscreen=False, type='dot'),
            dcc.Loading(dcc.Store(id='store-df_c'), fullscreen=False, type='dot'),
            dcc.Loading(dcc.Store(id='store-df_d'), fullscreen=False, type='dot'),
        ]),
        dbc.Col([
            dbc.Label('Plot view'),
            dcc.Dropdown(
                id='main-plot-view',
                options=[
                    {'label':'Time-Location','value':'time'},
                    {'label':'Demography','value':'demogr'},
                ], value='time' # default to time-location dimension
            )
        ])
    ]),
], style = card_style )

# app layout - use cards
app.layout = dbc.Container([
    card_page_header,
    html.Div(
        id='div-time',
        style={'flex':'auto'},
        children=time_view
    ),
    html.Div(
        id='div-demo',
        style={'flex':'auto'},
        children=demogr_view
    )
])

# callback for the data source
@app.callback(
    Input('main-data-source', 'value'),
    ServersideOutput('store-df_s', 'data'),
    ServersideOutput('store-df_c', 'data'),
    ServersideOutput('store-df_d', 'data'),
    memoize=True)
def get_data(value):
    if value==1:
        df_s,df_c,df_d = get_mysql_data()
    elif value==3:
        df_s,df_c,df_d = get_neo4j_data()
    else:
        df_s,df_c,df_d = get_mongo_data()
    return df_s,df_c,df_d

# callback control for viewing content
@app.callback(
    Output('div-time','style'),
    Output('div-demo','style'),
    Input('main-plot-view','value'),
    )
def render_content(value):
    if value == 'time':
        return {'display': 'block'}, {'display': 'none'}
    elif value == 'demogr':
        return {'display': 'none'}, {'display': 'block'}

# callback to create plots
@app.callback(
    Input('content','children')
    )
def update_figure(clicks,dummy):
    return clicks+1

if __name__ == '__main__':
    app.run_server()