# Import required libraries
# import pickle
# import copy
import pathlib
import dash
# import math
# import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
# import plotly.express as px
import plotly.graph_objs as go

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}], suppress_callback_exceptions=True
)
server = app.server

# Get Data
spo2_df = pd.read_csv(DATA_PATH.joinpath("data_spo2.csv"))
fev1_df = pd.read_csv(DATA_PATH.joinpath("data_fev1.csv"))
peak_df = pd.read_csv(DATA_PATH.joinpath("data_peak.csv"))
cough_df = pd.read_csv(DATA_PATH.joinpath("data_cough.csv"))
activity_df = pd.read_csv(DATA_PATH.joinpath("data_activity.csv"))

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-78.05, lat=42.54),
        zoom=7,
    ),
)

graph_layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        # html.Img(
                        #    src=app.get_asset_url("dash-logo.png"),
                        #   id="plotly-image",
                        #   style={
                        #       "height": "60px",
                        #       "width": "auto",
                        #       "margin-bottom": "25px",
                        #  },
                        # )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Spyro.ai",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Respiratory Monitoring System", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [

                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Filter by the time when the data was collected",
                            className="control_label",
                        ),
                        # dcc.Dropdown(
                        #    id="time_slider",
                        #    options=[
                        #        {"label": "Last Week", "value": 1},
                        #        {"label": "Last Month", "value": 2},
                        #        {"label": "Last Quarter", "value": 3},
                        #        {"label": "Last Year", "value": 4},
                        #        {"label": "All", "value": 0},
                        #    ],
                        #    multi=False,
                        #    value=2,
                        #    className="dcc_control",
                        #    #style={'width': "40%"}
                        # ),

                        dcc.RadioItems(
                            id="time_slider",
                            options=[
                                {"label": "1W", "value": 1},
                                {"label": "1M", "value": 2},
                                {"label": "1Q", "value": 3},
                                {"label": "1Y", "value": 4},
                                {"label": "All", "value": 0},
                            ],
                            value=4,
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),

                        # html.P("Filter by well status:", className="control_label"),

                    ],
                    className="pretty_container six columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [dcc.Graph(id="score_graph", figure={})],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="six columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="spo2_graph", figure={})],
                    className="pretty_container six columns",
                ),
                html.Div(
                    [dcc.Graph(id="lung_graph", figure={})],
                    className="pretty_container six columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="cough_graph", figure={})],
                    className="pretty_container six columns",
                ),
                html.Div(
                    [dcc.Graph(id="activity_graph", figure={})],
                    className="pretty_container six columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

page_2_layout = html.Div([
    html.H1('Page 2'),
    html.H3('Determine'),
    html.Table([
        html.Tr(
            [
                html.Td(''),
                html.Td('Green', colSpan=2),
                html.Td('Yellow', colSpan=2),
                html.Td('Red', colSpan=2)
            ]
        ),
        html.Tr(
            [
                html.Td(''),
                html.Td('min'),
                html.Td('max'),
                html.Td('min'),
                html.Td('max'),
                html.Td('min'),
                html.Td('max')
            ]
        ),
        html.Tr(
            [
                html.Td('FEV'),
                html.Td(
                    [
                        dcc.Input(id="input1", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(id="input1", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(id="input1", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(id="input1", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(id="input1", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(id="input1", type="text", placeholder="")
                    ]
                )
            ]
        ),
    ])

])

index_page = html.Div([
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return graph_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page


def filter_frame(df, value):
    dff = df.copy()
    if value == 1:
        dff = dff[-7:] if len(dff) >= 7 else dff
    elif value == 2:
        dff = dff[-30:] if len(dff) >= 30 else dff
    elif value == 3:
        dff = dff[-90:] if len(dff) >= 90 else dff
    elif value == 4:
        dff = dff[-365:] if len(dff) >= 365 else dff
    return dff


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


@app.callback(
    [Output('score_graph', 'figure'),
     Output('spo2_graph', 'figure'),
     Output('lung_graph', 'figure'),
     Output('cough_graph', 'figure'),
     Output('activity_graph', 'figure')],
    [Input(component_id='time_slider', component_property='value')]
)
def score_graph_(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    spo2_dff = spo2_df.copy()
    fev1_dff = fev1_df.copy()

    spo2_dff = filter_frame(spo2_df, option_slctd)
    fev1_dff = filter_frame(fev1_df, option_slctd)
    peak_dff = filter_frame(peak_df, option_slctd)
    cough_dff = filter_frame(cough_df, option_slctd)
    activity_dff = filter_frame(activity_df, option_slctd)

    # templates: ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]
    '''fig_spo2 = px.line(spo2_dff,
                       x='Date',
                       y='SPO2Values', 
                       template = "plotly",
                       title = "SPO2 Values over time")
    #fig_spo2.add_scatter(fev1_dff, x='Date', y='FEV1Values')'''
    # fig_spo2.update_xaxes(rangeslider_visible=True)

    # fig_spo2 = dict(data=data, layout=layout)
    fig_spo2 = make_go_graph(spo2_dff, 'Date', 'SPO2Values', title="SPO2 Values", name=None, color='#17BECF')
    fig_fev1 = make_go_graph(fev1_dff, 'Date', 'FEV1Values', title="FEV1 Values", name=None, color='#17BECF')
    # fig_peak = make_go_graph(peak_dff, 'Date', 'PEAKValues', title = "Peak Flow Values", name=None, color = '#17BECF')
    fig_lung = make_lung_graph([fev1_dff, peak_dff], ['Date', 'Date'], ['FEV1Values', 'PEAKValues'],
                               ['FEV1', 'Peak Flow'], colors=['#06EECF', '#17BECF'], title="Lung Functions")
    fig_cough = make_go_graph(cough_dff, 'Date', 'COUGHValues', title="Cough Counts", name=None, color='#17BECF')
    fig_activity = make_go_graph(activity_dff, 'Date', 'ACTIVITYValues', title="Active Minutes", name=None,
                                 color='#17BECF')
    return [fig_spo2, fig_fev1, fig_lung, fig_cough, fig_activity]


# Main
if __name__ == "__main__":
    app.run_server(debug=True, port=8025)
