from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
# modules
from server import app
from model.mysql import df_s,df_c
from model.mongo import df_s,df_c
from scripts.utils import *
from scripts.plots import *

#### UI OPTIONS ####

# extract state abbr and id
dc_state_ids = extract_dict(df_s,['state','state_id'])
# state abbrs include the US tag, which should be at top
ls_states = sorted(dc_state_ids.keys())
ls_states.insert(0, ls_states.pop(ls_states.index('US')))

dc_metrics = {
    'cases':'case_total',
    'deaths':'out_death',
    'severe cases':'out_severe',
    'infection rate':'pop_infect_rate',
    'severe case rate':'case_severe_rate',
    'case death rate':'case_death_rate',
    'severe case death rate':'severe_death_rate'
    }
ls_time_pts = sorted(df_s.month.dropna().unique())
dc_time_pts = { k : v for k, v in enumerate(ls_time_pts)}
dc_time_marks = { k : {'label': str(v)[0:-3] if k%3==0 else '', 'style':{}} for k, v in enumerate(ls_time_pts)}

# default options
curr_state = 'US'
curr_metric1 = 'cases'
curr_metric2 = 'deaths'
curr_metric3 = 'cases'
curr_time_pt = min(dc_time_pts.keys())

#### PAGE LAYOUT ####
# time series plot
card_time_series = dbc.Card([
    dbc.Row(dbc.Col(html.H3('Time, locatoin vs disease spread and severity'))),
    dbc.Row([
        # metric 1 selector
        html.H4('Time series plot'),
        dbc.Col([
            html.Div('metric 1 (left y-axis)'),
            dcc.Dropdown(
                id='dpdn-metric1-select',
                options=[{'label':k,'value':k} for k in dc_metrics.keys()],
                value=curr_metric1
            )
        ]),
        # state selector
        dbc.Col([
            html.B('location'),
            dcc.Dropdown(
                id='dpdn-state-select',
                options=[{'label':k,'value':k} for k in ls_states],
                value=curr_state
            )
        ]),
        # metric 2 selector
        dbc.Col([
            html.Div('metric 2 (right axis)'),
            dcc.Dropdown(
                id='dpdn-metric2-select',
                options=[{'label':k,'value':k} for k in dc_metrics.keys()],
                value=curr_metric2
            )
        ]),
    ]),
    dcc.Graph(id='fig-time-series'),
    html.P(),
    dbc.Row([
        html.H4('Choropleth plot'),
        dbc.Col([
            html.Div("Time "),
            dcc.Slider(
                id='sldr-time-series',
                min = min(dc_time_pts.keys()),
                max = max(dc_time_pts.keys()),
                step = len(dc_time_pts.keys()),
                value=curr_time_pt,
                marks=dc_time_marks,
                updatemode='drag'
            ),
        ]),
        dbc.Col([
            html.Div('metric for maps '),
            dcc.Dropdown(
                id='dpdn-metric3-select',
                options=[{'label':k,'value':k} for k in dc_metrics.keys()],
                value=curr_metric1
            ),
        ], width=4),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='fig-state-map')
        ]),
        dbc.Col([
            dcc.Graph(id='fig-county-map')
        ]),
    ]),
], style={'padding': '1rem 2rem'} )

# states and county map plot
card_map = dbc.Card([
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
    [Input('dpdn-state-select', 'value'),
     Input('dpdn-metric1-select', 'value'),
     Input('dpdn-metric2-select', 'value')]
    )
def gen_fig_time_series(a_state, metric1, metric2):
    # set the metrics
    if (metric1==metric2 or not metric2 or not metric1 ):
        # when both the same, or one is empty
        metrics = { dc_metrics.get(metric1):metric1 }
    else:
        # convert to a dict with {colname:tag name} for plotter
        metrics = { dc_metrics.get(metric1):metric1, dc_metrics.get(metric2):metric2}
    # get the plot
    return gen_state_time(df_s, a_state, metrics)
# make selected metrics grey out in the two metric dropdowns
def filter_metrics(val):
    '''construct a list of dict to disable option'''
    return [
        {'label': k, 'value': k, 'disabled': k == val}
        for k in dc_metrics.keys()
    ]
# reuse filter_metrics since both dropdowns are same
app.callback(
    Output('dpdn-metric1-select', 'options'),
    [Input('dpdn-metric2-select', 'value')]
    )(filter_metrics)
app.callback(
    Output('dpdn-metric2-select', 'options'),
    [Input('dpdn-metric1-select', 'value')]
    )(filter_metrics)

# CALLBACK for us-states level map
@app.callback(
    Output('fig-state-map', 'figure'),
    [Input('dpdn-metric3-select', 'value'),
     Input('sldr-time-series', 'value')]
)
def gen_fig_state_map(metric3, month):
    a_metric = [dc_metrics.get(metric3),metric3]
    a_month = dc_time_pts.get(month)
    return gen_state_map(df_s,a_metric,a_month)

# CALLBACK for state-counties level map
@app.callback(
    Output('fig-county-map', 'figure'),
    [Input('dpdn-state-select', 'value'),
     Input('dpdn-metric3-select', 'value'),
     Input('sldr-time-series', 'value')]
)
def gen_fig_county_map(a_state, metric3, month):
    a_state_id = dc_state_ids.get(a_state)
    a_month = dc_time_pts.get(month)
    a_metric = [dc_metrics.get(metric3),metric3]
    return gen_county_map(df_c,a_state,a_state_id,a_metric,a_month)