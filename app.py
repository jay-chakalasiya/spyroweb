# Import required libraries
import pickle
import copy
import pathlib
import dash
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px 

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

# Get Data
spo2_df = pd.read_csv(DATA_PATH.joinpath("data_spo2.csv"))
fev1_df = pd.read_csv(DATA_PATH.joinpath("data_fev1.csv"))


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



def spyro_layout(app):
    return html.Div(
        [
            dcc.Store(id="aggregate_data"),
            # empty Div to trigger javascript file for graph resizing
            html.Div(id="output-clientside"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url("dash-logo.png"),
                                id="plotly-image",
                                style={
                                    "height": "60px",
                                    "width": "auto",
                                    "margin-bottom": "25px",
                                },
                            )
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
                            dcc.Dropdown(
                                id="time_slider",
                                options=[
                                    {"label": "Last Week", "value": 1},
                                    {"label": "Last Month", "value": 2},
                                    {"label": "Last Quarter", "value": 3},
                                    {"label": "Last Year", "value": 4},
                                    {"label": "All", "value": 0},
                                ],
                                multi=False,
                                value=2,
                                className="dcc_control",
                                #style={'width': "40%"}
                            ),
                            dcc.RangeSlider(
                                id="year_slider",
                                min=1960,
                                max=2017,
                                value=[1990, 2010],
                                className="dcc_control",
                            ),
                            html.P("Filter by well status:", className="control_label"),
                            dcc.RadioItems(
                                id="well_status_selector",
                                options=[
                                    {"label": "All ", "value": "all"},
                                    {"label": "Active only ", "value": "active"},
                                    {"label": "Customize ", "value": "custom"},
                                ],
                                value="active",
                                labelStyle={"display": "inline-block"},
                                className="dcc_control",
                            ),
                            
                            dcc.Checklist(
                                id="lock_selector",
                                options=[{"label": "Lock camera", "value": "locked"}],
                                className="dcc_control",
                                value=[],
                            ),
                            html.P("Filter by well type:", className="control_label"),
                            dcc.RadioItems(
                                id="well_type_selector",
                                options=[
                                    {"label": "All ", "value": "all"},
                                    {"label": "Productive only ", "value": "productive"},
                                    {"label": "Customize ", "value": "custom"},
                                ],
                                value="productive",
                                labelStyle={"display": "inline-block"},
                                className="dcc_control",
                            ),
                            
                        ],
                        className="pretty_container four columns",
                        id="cross-filter-options",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [html.H6(int(spo2_df['SPO2Values'][0:1]),id="spo2_text"), html.P("SPO2")],
                                        id="spo2",
                                        className="mini_container",
                                    ),
                                    html.Div(
                                        [html.H6(id="peakflow_ext"), html.P("Peak Flow")],
                                        id="peakflow",
                                        className="mini_container",
                                    ),
                                    html.Div(
                                        [html.H6(int(fev1_df['FEV1Values'][0:1]*100), id="fev1_text"), html.P("FEV1")],
                                        id="fev1",
                                        className="mini_container",
                                    ),
                                    html.Div(
                                        [html.H6(id="excercise_text"), html.P("Excercise")],
                                        id="excercise",
                                        className="mini_container",
                                    ),
                                ],
                                id="info-container",
                                className="row container-display",
                            ),
                            html.Div(
                                [dcc.Graph(id="score_graph", figure={})],
                                id="countGraphContainer",
                                className="pretty_container",
                            ),
                        ],
                        id="right-column",
                        className="eight columns",
                    ),
                ],
                className="row flex-display",
            ),
            html.Div(
                [
                    html.Div(
                        [dcc.Graph(id="main_graph")],
                        className="pretty_container six columns",
                    ),
                    html.Div(
                        [dcc.Graph(id="individual_graph")],
                        className="pretty_container six columns",
                    ),
                ],
                className="row flex-display",
            ),
            html.Div(
                [
                    html.Div(
                        [dcc.Graph(id="pie_graph")],
                        className="pretty_container six columns",
                    ),
                    html.Div(
                        [dcc.Graph(id="aggregate_graph")],
                        className="pretty_container six columns",
                    ),
                ],
                className="row flex-display",
            ),
        ],
        id="mainContainer",
        style={"display": "flex", "flex-direction": "column"},
    )


app.layout = spyro_layout(app)


@app.callback(
    [Output('score_graph', 'figure')],
    [Input(component_id='time_slider', component_property='value')]
)
def score_graph_(option_slctd):
    print(option_slctd)
    print(type(option_slctd))
    
    spo2_dff = spo2_df.copy()
    
    
    if option_slctd==1:
        spo2_dff = spo2_dff[-7:] if len(spo2_dff)>=7 else spo2_dff
    elif option_slctd==2:
        spo2_dff = spo2_dff[-30:] if len(spo2_dff)>=30 else spo2_dff
    elif option_slctd==3:
        spo2_dff = spo2_dff[-90:] if len(spo2_dff)>=90 else spo2_dff
    elif option_slctd==4:
        spo2_dff = spo2_dff[-365:] if len(spo2_dff)>=365 else spo2_dff
    


    #templates: ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]
    fig_spo2 = px.line(spo2_dff,
                       x='Date',
                       y='SPO2Values', 
                       template = "plotly",
                       title = "SPO2 Values over time")
    fig_spo2.update_xaxes(rangeslider_visible=True)

    return [fig_spo2]



# Main
if __name__ == "__main__":
    app.run_server(debug=True, port=8025)