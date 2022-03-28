from dash import Dash, dcc, html
import plotly.graph_objects as go
import plotly.express as px
from plotly.graph_objs._figure import Figure
import pandas as pd
from weather_api import WeatherAPI
from utils import list_weather_data_to_df
import json
import dash_leaflet as dl
from dash.dependencies import Input, Output, State

NAMETABLE = {
    "temp": "Temperatur",
    "rain": "Regenfall",
    "max_temp": "Höchsttemperatur",
    "min_temp": "Mindesttemperatur",
    "cloudiness": "Wolken",
    "wind_speed": "Wind",
    "pop": "Niederschlagswarscheinlichtkeit",
}
DROPDOWN1 = ["Temperatur", "Regenfall", "Wolken", "Niederschlagswarscheinlichtkeit", "Wind"]

NAMETABLE_REVERSE = {v: k for k, v in NAMETABLE.items()}


def generate_figure(data: pd.DataFrame, fields: list[str], layout: dict, typ: str = "line"):
    traces = []
    for f in fields:
        traces.append(
            {
                "type": typ,
                "x": data.index,
                "y": data[NAMETABLE_REVERSE[f]],
                "name": f,
            }
        )
    fig = {"data": traces, "layout": layout}
    return fig


lat = 48
lon = 13


def run_dboard():

    url = "https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png"
    attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> '
    w = WeatherAPI()
    app = Dash(__name__)
    app.layout = html.Div(
        [
            html.H1(children="Wetterdashboard"),
            dl.Map(
                [dl.TileLayer(url=url, attribution=attribution), dl.LayerGroup(id="layer")],
                id="map",
                style={"width": "100%", "height": "50vh", "margin": "auto", "display": "block"},
                center=[48.1, 13.14],
                zoom=10,
            ),
            dcc.Dropdown(
                options=DROPDOWN1,
                value=["Temperatur"],
                id="xaxis-column",
                style={"color": "white"},
                multi=True,
            ),
            dcc.Graph(id="hourly_weather_line"),
            dcc.Graph(id="daily_weather_line"),
            dcc.Graph(id="hourly_weather_bar"),
            dcc.Graph(id="daily_weather_bar"),
        ]
    )

    @app.callback(
        Output("layer", "children"),
        [Input("map", "click_lat_lng")],
    )
    def map_click(click_lat_lng):

        if click_lat_lng is not None:
            global lat
            lat = click_lat_lng[0]
            global lon
            lon = click_lat_lng[1]
            return [
                dl.Marker(position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng))),
            ]
        return "-"

    @app.callback(
        Output("hourly_weather_line", "figure"),
        Output("daily_weather_line", "figure"),
        Output("hourly_weather_bar", "figure"),
        Output("daily_weather_bar", "figure"),
        Input("xaxis-column", "value"),
        [Input("map", "click_lat_lng")],
    )
    def update_plots(fieldnames: list, _):

        w.update(lat, lon)
        hourly_weather = list_weather_data_to_df(w.hourly_forecast)
        daily_weather = list_weather_data_to_df(w.daily_forecast)
        fieldname = fieldnames

        hourly_layout = {
            "paper_bgcolor": "rgb(26,25,25)",
            "plot_bgcolor": "rgb(26,25,25)",
            "font": {"color": "rgb(250,250,250"},
            "height": 300,
            "title": f"{fieldname} per h",
            "hovermode": "x unified",
            "margin": {"b": 60, "l": 30, "t": 70, "r": 0},  # Set margins to allow maximum space for the chart
            "legend": {  # Horizontal legens, positioned at the bottom to allow maximum space for the chart
                "orientation": "h",
                "x": 0,
                "y": 1.01,
                "yanchor": "bottom",
            },
            "xaxis": {"tickformat": "%H:%M %d/%m", "dtick": 3600000.0, "show_grid": True},
            "yaxis": {"automargin": True, "autorange": True},
            "hoverlabel": {"bgcolor": "rgb(26,25,25)", "font_size": 16},
        }
        hourly_fig_line = generate_figure(hourly_weather, fieldname, hourly_layout)
        hourly_fig_bar = generate_figure(hourly_weather, fieldname, hourly_layout, "bar")

        daily_layout = {
            "paper_bgcolor": "rgb(26,25,25)",
            "plot_bgcolor": "rgb(26,25,25)",
            "font": {"color": "rgb(250,250,250"},
            "height": 300,
            "title": f"Tages {fieldname}",
            "hovermode": "x unified",
            "margin": {"b": 60, "l": 30, "t": 70, "r": 0},  # Set margins to allow maximum space for the chart
            "legend": {  # Horizontal legens, positioned at the bottom to allow maximum space for the chart
                "orientation": "h",
                "x": 0,
                "y": 1.01,
                "yanchor": "bottom",
            },
            "xaxis": {"tickformat": "%d/%m/%Y", "dtick": 3600000.0 * 24, "show_grid": True},
            "yaxis": {"automargin": True, "autorange": True},
            "hover_data": ["temp"],
        }
        if "Temperatur" in fieldname:
            fieldname.extend(["Höchsttemperatur", "Mindesttemperatur"])
            fieldname.pop(fieldname.index("Temperatur"))
        daily_fig_line = generate_figure(daily_weather, fieldname, daily_layout)
        daily_fig_bar = generate_figure(daily_weather, fieldname, daily_layout, "bar")

        return hourly_fig_line, daily_fig_line, hourly_fig_bar, daily_fig_bar

    app.run_server(debug=False, host="0.0.0.0", port="80")
