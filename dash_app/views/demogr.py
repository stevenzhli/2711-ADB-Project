from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
# modules
from server import app
from model.mysql import df_d
from model.mongo import df_d
from scripts.utils import *
from scripts.plots import *

#### UI OPTIONS ####

df_d.race = df_d.race.fillna('Unknown')
ls_age = df_d.age.unique()
ls_sex = df_d.sex.unique()
ls_race = df_d.race.unique()

ls_dims = ['age','sex','race']

dc_metrics = {
    'cases':'case_total',
    'deaths':'out_death',
    'severe cases':'out_severe',
    'case death rate':'case_death_rate',
    'severe case rate':'case_severe_rate',
    'severe case death rate':'severe_death_rate'
    }

curr_dim1 = 'age'
curr_dim2 = 'sex'
curr_dim3 = 'race'
curr_metric1 = 'case death rate'
curr_metric2 = 'severe case rate'

#### LAYOUT ####

card_demogr = dbc.Card([
    dbc.Row(dbc.Col(html.H3('Demography vs disease severity'))),
    dbc.Row([
        # dimension 1 selector
        dbc.Col([
            html.Div('dimension 1 (y-axix)'),
            dcc.Dropdown(
                id='dpdn-dim1-select',
                options=[{'label':k,'value':k} for k in ls_dims],
                value=curr_dim1
            )
        ],width=2),
        # dimension 2 selector
        dbc.Col([
            html.Div('dimension 2 (color)'),
            dcc.Dropdown(
                id='dpdn-dim2-select',
                options=[{'label':k,'value':k} for k in ls_dims],
                value=curr_dim2
            )
        ],width=2),
        # dimension 3 selector
        dbc.Col([
            html.Div('dimension 3 (facet)'),
            dcc.Dropdown(
                id='dpdn-dim3-select',
                options=[{'label':k,'value':k} for k in ls_dims],
                value=curr_dim3
            )
        ],width=2),
    ]),
    dbc.Row([
        html.P(),
        html.H4('Plot 1'),
        dbc.Row([
            # metric 1 selector
            dbc.Col([
                dcc.Dropdown(
                    id='dpdn-metric1-demo-select',
                    options=[{'label':k,'value':k} for k in dc_metrics.keys()],
                    value=curr_metric1
                ),
            ],width=3,style=dict(display='inline-block')),
            dbc.Col([
                dbc.Button(
                    'Plot',
                    id='btn-metric1-plot',
                    className="me-2",
                    n_clicks=0
                )
            ]),
            dcc.Graph(id='fig-metric1')
        ]),
        html.H4('Plot 2'),
        dbc.Row([
            # metric 2 selector
            dbc.Col([
                dcc.Dropdown(
                    id='dpdn-metric2-demo-select',
                    options=[{'label':k,'value':k} for k in dc_metrics.keys()],
                    value=curr_metric2
                ),
            ],width=3,style=dict(display='inline-block')),
            dbc.Col([
                dbc.Button(
                    'Plot',
                    id='btn-metric2-plot',
                    className="me-2",
                    n_clicks=0
                )
            ]),
            dcc.Graph(id='fig-metric2')
        ]),
    ])
], style={'padding': '1rem 2rem'} )

# page layout
demogr_view = html.Div(
    [
        card_demogr,
    ]
)

#### CALLBACKS ####

@app.callback(
    Output('fig-metric1', 'figure'),
    Input('btn-metric1-plot', 'n_clicks'),
    State('dpdn-dim1-select', 'value'),
    State('dpdn-dim2-select', 'value'),
    State('dpdn-dim3-select', 'value'),
    State('dpdn-metric1-demo-select', 'value'))
def gen_fig(n_clicks,dim1, dim2, dim3, metric1):
    return gen_demogr_bar(df_d,[dim1,dim2,dim3],dc_metrics.get(metric1))

@app.callback(
    Output('fig-metric2', 'figure'),
    Input('btn-metric2-plot', 'n_clicks'),
    State('dpdn-dim1-select', 'value'),
    State('dpdn-dim2-select', 'value'),
    State('dpdn-dim3-select', 'value'),
    State('dpdn-metric2-demo-select', 'value'))
def gen_fig(n_clicks,dim1, dim2, dim3, metric2):
    return gen_demogr_bar(df_d,[dim1,dim2,dim3],dc_metrics.get(metric2))


# make selected metrics grey out in the two metric dropdowns
def filter_metrics(val):
    '''construct a list of dict to disable option'''
    return [
        {'label': k, 'value': k, 'disabled': k == val}
        for k in dc_metrics.keys()
    ]
# reuse filter_metrics since both dropdowns are same
app.callback(
    Output('dpdn-metric1-demo-select', 'options'),
    [Input('dpdn-metric2-demo-select', 'value')]
    )(filter_metrics)
app.callback(
    Output('dpdn-metric2-demo-select', 'options'),
    [Input('dpdn-metric1-demo-select', 'value')]
    )(filter_metrics)