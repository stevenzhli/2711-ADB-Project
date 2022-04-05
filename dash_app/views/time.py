from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.io
from server import app
from scripts.utils import extract_unique
from model.mysql import df_s,df_c
from scripts.plots import gen_state_time

# time-series: available options
all_states = extract_unique(df_s,'state')
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

# time-series: default options
curr_state = 'US'
curr_metric1 = 'cases'
curr_metric2 = 'deaths'

# time series plot
card_time_series = dbc.Card([
    dbc.Row(dbc.Col(html.H2('Time series plot for disease metrics'))),
    dbc.Row([
        # state selector
        dbc.Col([
            dbc.Label('State:'),
            dcc.Dropdown(
                id='state-select',
                options=[{'label':v,'value':v} for v in all_states],
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
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='fig-states-map',figure=plotly.io.read_json("assets/plot/state_map.json"))
        ]),
        dbc.Col([
            dcc.Graph(id='fig-county-map',figure=plotly.io.read_json("assets/plot/county_map.json"))
        ]),
    ])
])

# the page layout
time_view = html.Div(
    [
        card_time_series,
        card_map
    ]
)

# callback for time-state dropdown menus
@app.callback(
    Output('fig-time-series', 'figure'),
    [Input('btn-time-series', 'n_clicks')],
    [State('state-select', 'value'),
     State('metric1-select', 'value'),
     State('metric2-select', 'value')]
    )
def update_fig_time_series(n_clicks, state, metric1, metric2):
    curr_state = state
    df_filter = df_s[df_s['state'] == curr_state]
    # set the metrics, handle when selections are same or one is empty
    if (metric1==metric2 or not metric2 or not metric1 ):
        metrics = {all_metrics.get(metric1):metric1}
    else:
        metrics = { all_metrics.get(metric1):metric1, all_metrics.get(metric2):metric2}
    # get the plot
    return gen_state_time(df_filter, curr_state, metrics)

# make selected metric grey out
def filter_metrics(val):
    """
    construct a list of dict to disable option
    """
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
