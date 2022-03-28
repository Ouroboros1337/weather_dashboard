from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
from plotly.graph_objs._figure import Figure
import pandas as pd
from weather_api import WeatherAPI
from utils import list_weather_data_to_df
import json

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


def get_map():

    with open("./weather_dashboard/Austria.json", "r") as f:
        geo = json.load(f)

    bezirke = [i["properties"]["name"] for i in geo["features"]]

    fig = go.Figure(
        go.Scattergeo(
            locations=bezirke,
            geojson=geo,
            featureidkey="properties.name",
        )
    )
    fig.update_geos(
        resolution=50,
        showcoastlines=True,
        coastlinecolor="RebeccaPurple",
        showland=True,
        landcolor="LightGreen",
        showocean=True,
        oceancolor="LightBlue",
        showcountries=True,
        countrycolor="RebeccaPurple",
        scope="europe",
    )

    return fig


get_map()


def run_dboard():

    w = WeatherAPI()
    app = Dash(__name__)
    app.layout = html.Div(
        [
            html.H1(children="Wetterdashboard"),
            dcc.Graph(id="map", figure=get_map()),
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
        Output("hourly_weather_line", "figure"),
        Output("daily_weather_line", "figure"),
        Output("hourly_weather_bar", "figure"),
        Output("daily_weather_bar", "figure"),
        Input("xaxis-column", "value"),
    )
    def update_plots(fieldnames: list):

        w.update()
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
