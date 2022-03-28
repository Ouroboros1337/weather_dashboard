# A wrapper for the https://openweathermap.org/api weather api
# API documation: https://openweathermap.org/api/one-call-api
from requests import get
from utils import json_to_dict, timestamp_to_datetime
from constants import WEATHER_API_KEY, WEATHER_API_PARAMETERS
from exceptions import (
    NonEnabledException,
    MissingKeyException,
    InvalidResponseException,
)
from classtemplates import CurrentWeatherData, HourlyWeatherData, DailyWeatherData
from typing import Optional


class WeatherAPI(object):
    def __init__(self):
        if not WEATHER_API_KEY:
            raise MissingKeyException("There is no API key specified.")
        self.api_key = WEATHER_API_KEY
        self.lat = 0
        self.lat = 0

    def _get_data(self, lat: Optional[float] = None, lon: Optional[float] = None):
        request = "https://api.openweathermap.org/data/2.5/onecall"
        request += f"?appid={WEATHER_API_KEY}"
        for key, value in WEATHER_API_PARAMETERS.items():
            request += f"&{key}={value}"

        self.lat = 0 if lat is None else lat
        self.lon = 0 if lon is None else lon

        request += f"&lat={self.lat}"
        request += f"&lon={self.lon}"
        response = get(request)
        if "200" not in str(response):
            raise InvalidResponseException("API call returned invalid response")
        json_data = response.content
        self.data = json_to_dict(json_data)

    def _parse_data(self):

        if not self.data:
            self._get_data()

        current_data = self.data["current"]
        self.current_weather: CurrentWeatherData = CurrentWeatherData(
            lat=self.lat,
            lon=self.lon,
            timezone=self.data["timezone"],
            datetime=timestamp_to_datetime(current_data["dt"] + self.data["timezone_offset"]),
            timestamp=current_data["dt"] + self.data["timezone_offset"],
            temp=current_data["temp"],
            min_temp=current_data["temp"],
            max_temp=current_data["temp"],
            feels_like=current_data["feels_like"],
            humidity=current_data["humidity"],
            cloudiness=current_data["clouds"],
            wind_speed=current_data["wind_speed"],
            pressure=current_data["pressure"],
            rain_last_hour=current_data.get("rain") if current_data.get("rain") else 0,
            snow_last_hour=current_data.get("snow") if current_data.get("snow") else 0,
            pop=current_data.get("pop") * 100 if current_data.get("pop") else 0,
            weather_description=current_data["weather"][0]["description"],
        )
        self.hourly_forecast: list[HourlyWeatherData] = []
        for current_data in self.data["hourly"]:
            self.hourly_forecast.append(
                HourlyWeatherData(
                    lat=self.lat,
                    lon=self.lon,
                    timezone=self.data["timezone"],
                    datetime=timestamp_to_datetime(current_data["dt"] + self.data["timezone_offset"]),
                    timestamp=current_data["dt"] + self.data["timezone_offset"],
                    temp=current_data["temp"],
                    min_temp=current_data["temp"],
                    max_temp=current_data["temp"],
                    feels_like=current_data["feels_like"],
                    humidity=current_data["humidity"],
                    cloudiness=current_data["clouds"],
                    wind_speed=current_data["wind_speed"],
                    pressure=current_data["pressure"],
                    rain_last_hour=current_data.get("rain") if current_data.get("rain") else 0,
                    snow_last_hour=current_data.get("snow") if current_data.get("snow") else 0,
                    pop=current_data.get("pop") * 100 if current_data.get("pop") else 0,
                    weather_description=current_data["weather"][0]["description"],
                )
            )
        self.daily_forecast: list[DailyWeatherData] = []
        for current_data in self.data["daily"]:
            self.daily_forecast.append(
                DailyWeatherData(
                    lat=self.lat,
                    lon=self.lon,
                    timezone=self.data["timezone"],
                    datetime=timestamp_to_datetime(current_data["dt"] + self.data["timezone_offset"]),
                    timestamp=current_data["dt"] + self.data["timezone_offset"],
                    temp=current_data["temp"]["day"],
                    min_temp=current_data["temp"]["min"],
                    max_temp=current_data["temp"]["max"],
                    feels_like=current_data["feels_like"]["day"],
                    humidity=current_data["humidity"],
                    cloudiness=current_data["clouds"],
                    wind_speed=current_data["wind_speed"],
                    pressure=current_data["pressure"],
                    rain_last_hour=current_data.get("rain") if current_data.get("rain") else 0,
                    snow_last_hour=current_data.get("snow") if current_data.get("snow") else 0,
                    pop=current_data.get("pop") * 100 if current_data.get("pop") else 0,
                    weather_description=current_data["weather"][0]["description"],
                )
            )

    def update(self, lat: Optional[float] = None, lon: Optional[float] = None) -> None:
        if lat is not None and lon is not None:
            self.lat = lat
            self.lon = lon
            self._get_data(self.lat, self.lon)
        elif self.lat is not None and self.lon is not None:
            self._get_data(self.lat, self.lon)
        else:
            self._get_data()

        self._parse_data()
