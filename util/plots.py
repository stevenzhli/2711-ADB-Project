import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def save_state_map(df_s):
    df_s['month_str'] = df_s.month.astype(str)
    df_s = df_s.sort_values(by="month",ignore_index=True)

    fig = px.choropleth(
        df_s,
        locations='state',
        locationmode='USA-states',
        hover_name='state',
        color='case_total',
        color_continuous_scale=px.colors.sequential.Oranges,
        animation_frame="month_str",
        range_color=(0,20000),
        scope='usa')
    fig.write_html("./plot/state_map.html")


def save_county_map(df_c):
    # sort and convert to string for slider
    df_c['month_str'] = df_c.month.astype(str)
    df_c = df_c.sort_values(by="month",ignore_index=True)

    counties = json.load(open('./plot/geojson-counties-fips.json'))
    fig = px.choropleth(
        df_c,
        locations='county_id',
        geojson=counties,
        hover_name='county',
        color='case_total',
        color_continuous_scale=px.colors.sequential.Oranges,
        animation_frame="month_str",
        range_color=(0,200),
        scope='usa')
    fig.write_html("./plot/county_map.html")


def save_state_time(df_s):
    df_s = df_s.sort_values(by='population',ascending=False,ignore_index=True)
    fig = multi_plot(df_s,{'case_total':'total cases','out_death':'reported deaths'})
    fig.update_layout(
        yaxis=dict(range=[0,1e5]),
        yaxis2=dict(range=[0,2e3]),
    )
    fig.write_html("./plot/state_time.html")

def gen_demo_bar(df_d):
    return

def multi_plot(df, field_dict):
    """
    take a df and generate double-y axis multi-plot based on 'state' field
    Args:
        df (dataframe): dataframe containing the data
        dict_fields (dict): key, field name as in dataframe; value: name used in plot
    """
    fig = make_subplots(specs=[[{'secondary_y': True}]])
    states = df.state.unique().tolist()
    buttons = []
    i = 0
    fields = list(field_dict.keys())
    for state in states:
        df_tmp = df[df.state == state]
        df_tmp = df_tmp.sort_values('month')
        for field in fields:
            fig.add_trace(
                go.Scatter(
                    x=df_tmp.month,y=df_tmp[field],
                    name=state+' '+field_dict.get(field),mode='lines+markers',
                    line=dict(dash='solid',width=1),marker=dict(symbol='circle'),
                    ),
                secondary_y=False
            )
        # list of boolean indicate button which trace to show
        vis = [False] * len(states) * len(fields)
        vis[i*len(fields):(i+1)*len(fields)] = [True]*len(fields)
        button = dict(label=state,method='update',args=[{'visible': vis}])
        # add to button list
        buttons.append(button)
        i+=1
    fig.update_layout(
        updatemenus=[
            dict(
                type='buttons', direction='right', showactive=False,
                xanchor='left', yanchor='top', y=1.2,
                buttons=buttons[len(buttons)//2:],
            ),
            dict(
                type='buttons', direction='right',showactive=False,
                buttons=buttons[:len(buttons)//2],
                xanchor='left', yanchor='top',
                y=1.32
            )
        ]
    )
    return fig