from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from pymysql import NULL
# modules
from server import app
from scripts.utils import *
from scripts.plots import *

#### UI OPTIONS ####

# extract state abbr and id
dc_state_ids = {'MI': '26','IL': '17','MA': '25','GA': '13','FL': '12','LA': '22','NY': '36','OR': '41','CA': '6','CO': '8','NJ': '34','TX': '48','AZ': '4','ND': '38','OH': '39','IN': '18','NH': '33','AL': '1','NC': '37','TN': '47','PA': '42','WA': '53','IA': '19','MO': '29','MD': '24','WI': '55','CT': '9','HI': '15','UT': '49','NV': '32','MN': '27','KS': '20','AR': '5','ID': '16','SC': '45','NE': '31','PR': '72','OK': '40','AK': '2','ME': '23','KY': '21','NM': '35','WY': '56','VA': '51','DE': '10','RI': '44','MT': '30','VI': '78','GU': '66','SD': '46','DC': '11','VT': '50','MS': '28','WV': '54','US': '0'}
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
ls_time_pts = sorted(['2021-12-15', '2022-01-15', '2021-07-15', '2021-08-15',
       '2021-01-15', '2021-02-15', '2020-12-15', '2021-03-15',
       '2020-11-15', '2021-09-15', '2021-10-15', '2022-02-15',
       '2020-09-15', '2021-06-15', '2020-04-15', '2020-07-15',
       '2021-04-15', '2020-08-15', '2021-11-15', '2020-10-15',
       '2021-05-15', '2020-06-15', '2020-03-15', '2020-05-15',
       '2020-01-15', '2020-02-15'])
dc_time_pts = { k : v for k, v in enumerate(ls_time_pts)}
dc_time_marks = { k : {'label': str(v)[0:-3] if k%3==0 else '', 'style':{}} for k, v in enumerate(ls_time_pts)}

# default options
curr_state = 'US'
curr_metric1 = 'cases'
curr_metric2 = 'deaths'
curr_metric3 = 'severe case rate'
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
                value=curr_metric3
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

# CALLBACK for time-state time series plot
@app.callback(
    Output('fig-time-series', 'figure'),
    Input("store-df_s", "data"),
    Input('dpdn-state-select', 'value'),
    Input('dpdn-metric1-select', 'value'),
    Input('dpdn-metric2-select', 'value'),
    )
def gen_fig_time_series(df, a_state, metric1, metric2):
    # set the metrics
    if (metric1==metric2 or not metric2 or not metric1 ):
        # when both the same, or one is empty
        metrics = { dc_metrics.get(metric1):metric1 }
    else:
        # convert to a dict with {colname:tag name} for plotter
        metrics = { dc_metrics.get(metric1):metric1, dc_metrics.get(metric2):metric2}
    # get the plot
    return gen_state_time(df, a_state, metrics)

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
    Input('dpdn-metric2-select', 'value'),
    )(filter_metrics)
app.callback(
    Output('dpdn-metric2-select', 'options'),
    Input('dpdn-metric1-select', 'value'),
    )(filter_metrics)

# CALLBACK for us-states level map
@app.callback(
    Output('fig-state-map', 'figure'),
    Input("store-df_s", "data"),
    Input('dpdn-metric3-select', 'value'),
    Input('sldr-time-series', 'value'),
)
def gen_fig_state_map(df, metric3, month):
    a_metric = [dc_metrics.get(metric3),metric3]
    a_month = dc_time_pts.get(month)
    return gen_state_map(df,a_metric,a_month)

# CALLBACK for state-counties level map
@app.callback(
    Output('fig-county-map', 'figure'),
    Input("store-df_c", "data"),
    Input('dpdn-state-select', 'value'),
    Input('dpdn-metric3-select', 'value'),
    Input('sldr-time-series', 'value'),
)
def gen_fig_county_map(df, a_state, metric3, month):
    a_state_id = dc_state_ids.get(a_state)
    a_month = dc_time_pts.get(month)
    a_metric = [dc_metrics.get(metric3),metric3]
    return gen_county_map(df,a_state,a_state_id,a_metric,a_month)