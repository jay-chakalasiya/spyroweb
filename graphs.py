import plotly.graph_objs as go
import pandas as pd

def make_go_graph(df, x_column, y_column, title=None, name=None, color='#17BECF'):
    trace = go.Scatter(
        x=df[x_column],
        y=df[y_column],
        name=name,
        line=dict(color=color),
        opacity=0.8)
    data = [trace]
    layout = dict(
        title=title,
        line_shape="spline",
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=3,
                         label='3m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=12,
                         label='1Y',
                         step='month',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(),
            type='date'
        )
    )

    fig = dict(data=data, layout=layout)
    return fig

def make_lung_graph(dfs, x_columns, y_columns, names, colors=None, title=None):
    if colors is None:
        colors = ['#17EECF', '#17BECF']
    trace1 = go.Scatter(
        x=dfs[0][x_columns[0]],
        y=dfs[0][y_columns[0]],
        name=names[0],
        line=dict(color=colors[0]),
        opacity=0.8)
    trace2 = go.Scatter(
        x=dfs[1][x_columns[1]],
        y=dfs[1][y_columns[1]],
        name=names[1],
        line=dict(color=colors[1]),
        opacity=0.8)
    data = [trace1, trace2]

    layout = dict(
        title=title,
        line_shape="spline",
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=3,
                         label='3m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=12,
                         label='1Y',
                         step='month',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(),
            type='date'
        )
    )

    fig = dict(data=data, layout=layout)
    return fig



