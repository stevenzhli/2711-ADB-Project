import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from util import utils,plots

app = dash.Dash(__name__)

# read in the data
utils.get_mysql_data('root','testpassmysql')


app.layout = html.Div(
    [
        html.H1('标题1'),
        html.H1('标题2'),
        dcc.Dropdown(
            options=[
                {'label':'MySQL','value':1},
                {'label':'MongoDB','value':2},
                {'label':'Neo4J','value':3},
            ]
        ),
        dcc.Graph(figure=fig)
    ],
)


if __name__ == '__main__':
    app.run_server()