import json, math
import plotly.express as px, plotly.graph_objects as go
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

def gen_state_time(df_s,location,metrics):
    df_tmp = df_s[df_s.state == location].sort_values('month')
    fig = double_y_time_plot(df_tmp,'month',location,metrics)
    return fig

def double_y_time_plot(df, time, location, metrics):
    """
    take a df and generate double-y axis multi-plot for a location
    handles if single metric is provided
    Args:
        df (dataframe): dataframe containing the data
        time (string): df field to use as time x-axis
        location (string): location name to show in plot
        metrics (dict): df fields to display as metrics in y-axis
                        key, field name as in dataframe; value: metric name to show in plot
    """
    # unpack the metrics
    fields = list(metrics.keys())
    # produce the figure
    x=df[time]
    if(len(metrics)==1):
        y1=df[fields[0]]
    else:
        y1=df[fields[0]]
        y2=df[fields[1]]
    fig = make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(
        go.Scatter(
            x=x,y=y1,
            name=location+' '+metrics.get(fields[0]),mode='lines+markers',
            line=dict(dash='solid',width=1),marker=dict(symbol='circle'),
            ),
        secondary_y=False
    )
    # place legend at top
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="auto"
    ))
    if(len(metrics)==1):
        return fig
    else:
        fig.add_trace(
            go.Scatter(
                x=x,y=y2,
                name=location+' '+metrics.get(fields[1]),mode='lines+markers',
                line=dict(dash='dot',width=1),marker=dict(symbol='x'),
                ),
            secondary_y=True
        )
        # set upper bound for y-axes
        # fig.update_layout(
        #     yaxis=dict(range=[0,scale_y_scope(y1)]),
        #     yaxis2=dict(range=[0,scale_y_scope(y2)]),
        # )
        return fig

# def scale_y_scope(list):
#     """
#     scale the y-axis to 1.1x of the maximum value in the provided list
#     """
#     mv = max(list)
#     if(mv>100):
#         digits = math.ceil(math.log10(mv))
#         return round(mv*1.1,-(digits-2))
#     elif(mv>10):
#         return (mv//5+1)*5
#     elif(mv<1): # <1, rate
#         return (math.ceil(mv*10)/10)