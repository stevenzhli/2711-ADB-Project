from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.io
from sklearn import metrics
from server import app
from scripts.utils import extract_dict
from model.mysql import df_s,df_c
from scripts.plots import *

#### UI OPTIONS ####

# extract state abbr and id
state_ids = extract_dict(df_s,['state','state_id'])
# state abbrs include the US tag, which should be at top
all_states = sorted(state_ids.keys())
all_states.insert(0, all_states.pop(all_states.index('US')))

all_metrics = {
    'cases':'case_total',
    'deaths':'out_death',
    'severe cases':'out_severe',
    'infection rate':'pop_infect_rate',
    'severe case rate':'case_severe_rate',
    'case death rate':'case_death_rate',
    'severe case death rate':'severe_death_rate'
    }

# default options
curr_state = 'US'
curr_metric1 = 'cases'
curr_metric2 = 'deaths'
curr_metric3 = 'cases'

#### PAGE LAYOUT ####
# time series plot
card_time_series = dbc.Card([
    dbc.Row(dbc.Col(html.H2('Time series plot for disease metrics'))),
    dbc.Row([
        # state selector
        dbc.Col([
            dbc.Label('State:'),
            dcc.Dropdown(
                id='state-select',
                options=[{'label':k,'value':k} for k in all_states],
                value=curr_state
            )
        ]),
        # metric 1 selector
        dbc.Col([
            dbc.Label('Metric1:'),
            dcc.Dropdown(
                id='metric1-select',
                options=[{'label':k,'value':k} for k in all_metrics.keys()],
                value=curr_metric1
            )
        ]),
        # metric 2 selector
        dbc.Col([
            dbc.Label('Metric2:'),
            dcc.Dropdown(
                id='metric2-select',
                options=[{'label':k,'value':k} for k in all_metrics.keys()],
                value=curr_metric2
            )
        ]),
        # button to submit the selected options
        dbc.Col([
            dbc.Button('Submit', id='btn-time-series', n_clicks=0)
        ],align='end'),
    ]),
    dcc.Graph(id='fig-time-series')
    ],
    style={"padding": "1rem 1rem"}
)

# states and county map plot
card_map = dbc.Card([
    dbc.Row(dbc.Col(html.H2('Map of disease metrics'))),
    dbc.Row([
        dbc.Label('Metric:'),
        dcc.Dropdown(
            id='metric3-select',
            options=[{'label':k,'value':k} for k in all_metrics.keys()],
            value=curr_metric1
        )
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='fig-state-map')
        ]),
        dbc.Col([
            dcc.Graph(id='fig-county-map')
        ]),
    ])
])

# page layout
time_view = html.Div(
    [
        card_time_series,
        card_map
    ]
)

#### CALLBACKS ####

# CALLBACK for time-state dropdown menus
@app.callback(
    Output('fig-time-series', 'figure'),
    [Input('btn-time-series', 'n_clicks')],
    [State('state-select', 'value'),
     State('metric1-select', 'value'),
     State('metric2-select', 'value')]
    )
def gen_fig_time_series(n_clicks, a_state, metric1, metric2):
    # set the metrics
    if (metric1==metric2 or not metric2 or not metric1 ):
        # when both the same, or one is empty
        metrics = { all_metrics.get(metric1):metric1 }
    else:
        # convert to a dict with {colname:tag name} for plotter
        metrics = { all_metrics.get(metric1):metric1, all_metrics.get(metric2):metric2}
    # get the plot
    return gen_state_time(df_s, a_state, metrics)
# make selected metrics grey out in the two metric dropdowns
def filter_metrics(val):
    '''construct a list of dict to disable option'''
    return [
        {"label": k, "value": k, "disabled": k == val}
        for k in all_metrics.keys()
    ]
# reuse filter_metrics since both dropdowns are same
app.callback(
    Output("metric1-select", "options"),
    [Input("metric2-select", "value")]
    )(filter_metrics)
app.callback(
    Output("metric2-select", "options"),
    [Input("metric1-select", "value")]
    )(filter_metrics)

# CALLBACK for us-states level map
@app.callback(
    Output('fig-state-map', 'figure'),
    [Input('metric3-select', 'value')]
)
def gen_fig_state_map(metric3):
    metric = [all_metrics.get(metric3),metric3]
    return gen_state_map(df_s,metric)

# CALLBACK for state-counties level map
@app.callback(
    Output('fig-county-map', 'figure'),
    [Input('state-select', 'value'),
     Input('metric3-select', 'value')]
)
def gen_fig_county_map(a_state, metric3):
    a_state_id = state_ids.get(a_state)
    metric = [all_metrics.get(metric3),metric3]
    return gen_county_map(df_c,a_state_id,metric)