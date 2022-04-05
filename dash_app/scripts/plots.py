import json, math
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

def gen_demogr_bar(df, dims, metric):
    # get non-empty dimensions
    real_dims = [i for i in dims if i]
    n_dims = len(real_dims)
    # groupby
    df_tmp = df.groupby(real_dims).sum().reset_index()
    # calculate if rate metrics
    if metric[-4:] == 'rate':
        match metric:
            case 'case_death_rate':
                df_tmp[metric] = df_tmp.out_death/df_tmp.out_total
            case 'case_severe_rate':
                df_tmp[metric] = df_tmp.out_severe/df_tmp.out_total
            case 'severe_death_rate':
                df_tmp[metric] = df_tmp.out_death/df_tmp.out_severe
    # generate plot
    if n_dims == 1:
        fig = px.bar(
            data_frame=df_tmp,
            y=real_dims[0],
            x=metric,
            barmode='group'
        )
    elif n_dims == 2:
        fig = px.bar(
            data_frame=df_tmp,
            y=real_dims[0],
            x=metric,
            color=real_dims[1],
            barmode='group'
        )
    elif n_dims == 3:
        fig = px.bar(
            data_frame=df_tmp,
            y=real_dims[0],
            x=metric,
            color=real_dims[1],
            facet_col=real_dims[2],
            barmode='group'
        )
    fig.update_layout(xaxis_title=None,margin=dict(l=10,r=10,t=50,b=10))
    return fig

def gen_state_map(df,metric,month):
    '''
    generate state level map
    metric: list of the metric's [colname, tag name in plot]
    '''
    # ensure fixed upper bound
    upper = df[df['state']!='US'][metric[0]].max()
    # filter by month
    df_tmp = df[df.month==month]
    fig = px.choropleth(
        df_tmp,
        locations='state',
        locationmode='USA-states',
        color=metric[0],
        color_continuous_scale=px.colors.sequential.Oranges,
        range_color=(0,upper),
        scope='usa',
        title="US "+metric[1],
        labels={metric[0]:''},
        hover_name='state',
        hover_data={metric[0]:True,'month':False,'state':False}
    )
    fig.update_layout(title=dict(xanchor='center',x=0.5),margin=dict(l=10,r=10,t=50,b=10))
    # fig.write_json(os.path.join('assets','plot','state_map.json'))
    return fig

def gen_county_map(df,state,state_id,metric,month):
    '''
    generate county level map of given state_id
    metric: list of the metric's [colname, tag name in plot]
    '''
    if state_id == 0:
        return go.Figure()
    # filter by state_id
    df_tmp = df[df.state_id==state_id]
    # ensure fixed upper bound
    upper = df_tmp[metric[0]].max()
    # filter by month
    df_tmp = df_tmp[df_tmp.month==month]

    # get county level geojson
    area = json.load(open(os.path.join('assets','geojson',str(state_id).zfill(2)+'.json')))
    fig = px.choropleth(
        df_tmp,
        locations='county_id',
        geojson=area,
        color=metric[0],
        color_continuous_scale=px.colors.sequential.Oranges,
        title=state+" "+metric[1],
        range_color=(0,upper),
        scope='usa',
        fitbounds='locations',
        labels={metric[0]:''},
        hover_name='county',
        hover_data={metric[0]:True,'month':False,'county_id':False}
    )
    fig.update_layout(title=dict(xanchor='center',x=0.5),margin=dict(l=10,r=10,t=50,b=10))

    # fig.write_json(os.path.join('assets','plot','state'+state_id+'.json'))
    return fig

def gen_state_time(df,state_name,metrics):
    df_tmp = df[df.state == state_name].sort_values('month')
    fig = __double_y_time_plot(df_tmp,'month',state_name,metrics)
    return fig

def __double_y_time_plot(df, time, location, metrics):
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
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="auto"
        ),
        yaxis=dict(
            autorange=True
        ),
        margin=dict(l=10,r=10,t=50,b=10)
    )
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