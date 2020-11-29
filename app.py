
import pathlib
import dash
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


from graphs import make_go_graph, make_lung_graph
from database import db_mock, db_transform
from config import graph_config

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}], suppress_callback_exceptions=True
)
server = app.server

database = db_mock()#db_transform("mongodb://10.0.0.179:27017", 'spyro', '5f7f85757391fd43388dd7c0')
config = graph_config()


mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"


graph_layout = html.Div(
    [
        html.Button(dcc.Link('Go to plan screen', href='/plan'), id="graph_screen_button"),
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
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

                    ],
                    className="pretty_container six columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [dcc.Graph(id="lung_function_graph", figure={})],
                    className="pretty_container six columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="o2_graph", figure={})],
                    className="pretty_container six columns",
                ),
                html.Div(
                    [dcc.Graph(id="pulse_graph", figure={})],
                    className="pretty_container six columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="activity_graph", figure={})],
                    className="pretty_container six columns",
                ),
                html.Div(
                    [dcc.Graph(id="sleep_graph", figure={})],
                    className="pretty_container six columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

plan_layout = html.Form([
    html.Button(dcc.Link('Go to graph screen', href='/'), id="plan_screen_button"),
    html.H1('Treatment Plan'),
    html.H3('Zone Values'),
    html.Table([
        html.Tr(
            [
                html.Td(''),
                html.Td('Green Zone', colSpan=2),
                html.Td('Yellow Zone', colSpan=2),
                html.Td('Red Zone', colSpan=2)
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
                        dcc.Input(name="fev_green_rangeLow", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="fev_green_rangeHigh", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="fev_yellow_rangeLow", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="fev_yellow_rangeHigh", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="fev_red_rangeLow", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="fev_red_rangeHigh", type="text", placeholder="")
                    ]
                )
            ]
        ),
        html.Tr(
            [
                html.Td('PEF'),
                html.Td(
                    [
                        dcc.Input(name="pef_green_rangeLow", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="pef_green_rangeHigh", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="pef_yellow_rangeLow", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="pef_yellow_rangeHigh", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="pef_red_rangeLow", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="pef_red_rangeHigh", type="text", placeholder="")
                    ]
                )
            ]
        ),
        html.Tr(
            [
                html.Td('O2'),
                html.Td(
                    [
                        dcc.Input(name="o2_green_rangeLow", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="o2_green_rangeHigh", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="o2_yellow_rangeLow", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="o2_yellow_rangeHigh", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="o2_red_rangeLow", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="o2_red_rangeHigh", type="text", placeholder="")
                    ]
                )
            ]
        ),
        html.Tr(
            [
                html.Td('Pulse'),
                html.Td(
                    [
                        dcc.Input(name="pulse_green_rangeLow", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="pulse_green_rangeHigh", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="pulse_yellow_rangeLow", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="pulse_yellow_rangeHigh", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="pulse_red_rangeLow", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="pulse_red_rangeHigh", type="text", placeholder="")
                    ]
                )
            ]
        ),
        html.Tr(
            [
                html.Td('Activity Goal %'),
                html.Td(
                    [
                        dcc.Input(name="activityGoalPercentage_green_rangeLow", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="activityGoalPercentage_green_rangeHigh", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="activityGoalPercentage_yellow_rangeLow", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="activityGoalPercentage_yellow_rangeHigh", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="activityGoalPercentage_red_rangeLow", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="activityGoalPercentage_red_rangeHigh", type="text", placeholder="")
                    ]
                )
            ]
        ),
        html.Tr(
            [
                html.Td('Sleep'),
                html.Td(
                    [
                        dcc.Input(name="totalSleepMinutes_green_rangeLow", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="totalSleepMinutes_green_rangeHigh", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="totalSleepMinutes_yellow_rangeLow", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="totalSleepMinutes_yellow_rangeHigh", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="totalSleepMinutes_red_rangeLow", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="totalSleepMinutes_red_rangeHigh", type="text", placeholder="")
                    ]
                )
            ]
        ),
    ]),
    html.H3('Medications'),
    html.Table([
        html.Tr(
            [
                html.Td('Name'),
                html.Td('Quantity Type'),
                html.Td('Green Zone'),
                html.Td('Yellow Zone'),
                html.Td('Red Zone'),
            ]
        ),

        html.Tr(
            [

                html.Td(
                    [
                        dcc.Input(name="medicines_name_1", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="medicines_quantityType_1", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="medicines_green_quantity_1", type="text", placeholder="quantity")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="medicines_yellow_quantity_1", type="text", placeholder="quantity")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="medicines_red_quantity_1", type="text", placeholder="quantity")
                    ]
                ),
            ],
        ),
        html.Tr(
            [

                html.Td(''),
                html.Td(''),
                html.Td(
                    [
                        dcc.Input(name="medicines_green_timeOfDay_1", type="text", placeholder="time of day")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="medicines_yellow_timeOfDay_1", type="text", placeholder="time of day")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="medicines_red_timeOfDay_1", type="text", placeholder="time of day")
                    ]
                )
            ],
        ),

        html.Tr(
            [

                html.Td(
                    [
                        dcc.Input(name="medicines_name_2", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="medicines_quantityType_2", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="medicines_green_quantity_2", type="text", placeholder="quantity")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="medicines_yellow_quantity_2", type="text", placeholder="quantity")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="medicines_red_quantity_2", type="text", placeholder="quantity")
                    ]
                ),
            ],
        ),
        html.Tr(
            [

                html.Td(''),
                html.Td(''),
                html.Td(
                    [
                        dcc.Input(name="medicines_green_timeOfDay_2", type="text", placeholder="time of day")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="medicines_yellow_timeOfDay_2", type="text", placeholder="time of day")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="medicines_red_timeOfDay_2", type="text", placeholder="time of day")
                    ]
                )
            ],
        ),

        html.Tr(
            [

                html.Td(
                    [
                        dcc.Input(name="medicines_name_3", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="medicines_quantityType_3", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="medicines_green_quantity_3", type="text", placeholder="quantity")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="medicines_yellow_quantity_3", type="text", placeholder="quantity")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="medicines_red_quantity_3", type="text", placeholder="quantity")
                    ]
                ),
            ],
        ),
        html.Tr(
            [

                html.Td(''),
                html.Td(''),
                html.Td(
                    [
                        dcc.Input(name="medicines_green_timeOfDay_3", type="text", placeholder="time of day")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="medicines_yellow_timeOfDay_3", type="text", placeholder="time of day")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="medicines_red_timeOfDay_3", type="text", placeholder="time of day")
                    ]
                )
            ],
        )

    ]),
    html.H3('Measurements'),
    html.Table([
        html.Tr(
            [
                html.Td('Name'),
                html.Td('Green Zone Frequency'),
                html.Td('Yellow Zone Frequency'),
                html.Td('Red Zone Frequency'),
            ]
        ),

        html.Tr(
            [
                html.Td(
                    [
                        dcc.Input(name="measurements_typeName_1", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="measurements_green_frequency_1", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="measurements_yellow_frequency_1", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="measurements_red_frequency_1", type="text", placeholder="")
                    ]
                ),

            ],
        ),
        html.Tr(
            [
                html.Td(
                    [
                        dcc.Input(name="measurements_typeName_2", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="measurements_green_frequency_2", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="measurements_yellow_frequency_2", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="measurements_red_frequency_2", type="text", placeholder="")
                    ]
                ),

            ],
        ),
        html.Tr(
            [
                html.Td(
                    [
                        dcc.Input(name="measurements_typeName_3", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="measurements_green_frequency_3", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="measurements_yellow_frequency_3", type="text", placeholder="")
                    ]
                ),
                html.Td(
                    [
                        dcc.Input(name="measurements_red_frequency_3", type="text", placeholder="")
                    ]
                ),

            ],
        ),
    ]),
    html.Br(),
    html.Button('Submit', type='submit')
], action='http://127.0.0.1:3000/unsecured/recordPlanTest', method='post')

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/plan':
        return plan_layout
    else:
        return graph_layout



@app.callback(
    [Output('lung_function_graph', 'figure'),
     Output('o2_graph', 'figure'),
     Output('pulse_graph', 'figure'),
     Output('activity_graph', 'figure'),
     Output('sleep_graph', 'figure')],
    [Input(component_id='time_slider', component_property='value')]
)
def score_graph_(option_slctd):

    fig_O2 = make_go_graph(
        database.data[option_slctd]['O2'],
        config.cols['index_col'],
        config.cols['O2'],
        title=config.titles['O2'],
        name=None,
        color='#17BECF'
    )

    fig_PULSE = make_go_graph(
        database.data[option_slctd]['PULSE'],
        config.cols['index_col'],
        config.cols['PULSE'],
        title=config.titles['PULSE'],
        name=None,
        color='#17BECF'
    )

    fig_LUNG_FUNCTION = make_lung_graph(
        [database.data[option_slctd]['FEV1'], database.data[option_slctd]['PEF']],
        [config.cols['index_col'], config.cols['index_col']],
        [config.cols['FEV1'], config.cols['PEF']],
        ['FEV1', 'Peak Flow'],
        colors=['#06EECF', '#17BECF'],
        title=config.titles['LUNG_GRAPH']
    )

    fig_SLEEP = make_go_graph(
        database.data[option_slctd]['SLEEP'],
        config.cols['index_col'],
        config.cols['SLEEP'],
        title=config.titles['SLEEP'],
        name=None,
        color='#17BECF'
    )

    fig_ACTIVITY = make_go_graph(
        database.data[option_slctd]['ACTIVITY'],
        config.cols['index_col'],
        config.cols['ACTIVITY'],
        title=config.titles['ACTIVITY'],
        name=None,
        color='#17BECF'
    )

    return [fig_LUNG_FUNCTION, fig_O2, fig_PULSE, fig_ACTIVITY, fig_SLEEP]


# Main
if __name__ == "__main__":
    app.run_server(debug=True, port=8025)
