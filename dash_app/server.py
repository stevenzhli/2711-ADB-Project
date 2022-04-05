import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
    # suppress_callback_exceptions=True
)

# webpage title
app.title = 'COVID-19 US Case Surveillance DW'

server = app.server
