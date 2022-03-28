# Here are some utility functions
from typing import Union
from json import loads
from datetime import datetime
from classtemplates import (
    DateTime,
    HourlyWeatherData,
    CurrentWeatherData,
    DailyWeatherData,
)
import pandas as pd


def json_to_dict(json_data: bytes) -> dict:
    return loads(json_data.decode("utf-8"), strict=False)


def timestamp_to_datetime(timestamp: int) -> DateTime:
    date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
    time = datetime.utcfromtimestamp(timestamp).strftime("%H:%M")
    return DateTime(date, time, f"{date} {time}")


def list_weather_data_to_df(data) -> pd.DataFrame:
    df = pd.DataFrame.from_records([d.__dict__() for d in data])
    df.set_index("index", inplace=True)
    return df
