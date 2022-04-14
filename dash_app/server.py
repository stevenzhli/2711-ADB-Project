import dash_bootstrap_components as dbc
from dash_extensions.enrich import Dash, Output, Input, Trigger, ServersideOutput

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SANDSTONE],
    prevent_initial_callbacks=True
    # suppress_callback_exceptions=True
)

# webpage title
app.title = 'COVID-19 US Case Surveillance DW'

server = app.server
