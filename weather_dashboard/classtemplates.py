# templates for classes
from dataclasses import dataclass
from typing import NamedTuple
from constants import TEMP_UNIT, SPEED_UNIT, LANGUAGE_CODE


class DateTime(NamedTuple):
    """A named tuple containing date and time and datetime as strings"""

    date: str
    time: str
    datetime: str


@dataclass
class WeatherData:
    lat: float
    lon: float
    timezone: str
    datetime: DateTime
    timestamp: int
    temp: float
    max_temp: float
    min_temp: float
    feels_like: float
    humidity: float
    cloudiness: float
    wind_speed: float
    pressure: float
    pop: float
    rain_last_hour: float
    snow_last_hour: float
    weather_description: str

    def __dict__(self):
        return {
            "date": self.datetime[0],
            "time": self.datetime[1],
            "index": self.datetime[2],
            "temp": self.temp,
            "max_temp": self.max_temp,
            "min_temp": self.min_temp,
            "humidity": self.humidity,
            "cloudiness": self.cloudiness,
            "wind_speed": self.wind_speed,
            "pressure": self.pressure,
            "pop": self.pop,
            "rain": self.rain_last_hour,
        }


class CurrentWeatherData(WeatherData):
    def __repr__(self) -> str:

        if LANGUAGE_CODE == "de":
            return (
                f"Das heutige Wetter am {self.datetime.date} um {self.datetime.time} Uhr:\n"
                f"Wir haben {self.temp}{TEMP_UNIT} mit einer Luftfeuchtigkeit von {self.humidity}% und einem Luftdruck von {self.pressure} hPa.\n"
                f"Der Himmel ist zu {self.cloudiness}% mit Wolken bedeckt.\n"
                f'"{self.weather_description}"\n'
                f"Der Wind bläst mit {self.wind_speed}{SPEED_UNIT}, es fühlt sich an als hätten wir {self.feels_like}{TEMP_UNIT}.\n"
                f"In der letzten Stunde {f'hat es ungefähr {self.rain_last_hour} mm geregnet' if self.rain_last_hour else f'hatten wir ungefähr {self.snow_last_hour} mm Schneefall' if self.snow_last_hour else 'hat es nicht geregnet'}."
            )
        else:
            return (
                f"The current weather on {self.datetime.date} at {self.datetime.time} o'clock:\n"
                f"We have a temperature of {self.temp}{TEMP_UNIT} with a humidity of {self.humidity}% and a pressure of {self.pressure} hPa.\n"
                f"We have a cloudiness of {self.cloudiness}%\n"
                f'"{self.weather_description}"\n'
                f"The wind is currently blowing with {self.wind_speed}{SPEED_UNIT}, it feels like we have {self.feels_like}{TEMP_UNIT}.\n"
                f"In the last hour it {f'rained approximately {self.rain_last_hour} mm' if self.rain_last_hour else f'snowed approximately {self.snow_last_hour} mm' if self.snow_last_hour else 'did not rain or snow'}."
            )


class HourlyWeatherData(WeatherData):
    def __repr__(self) -> str:

        if LANGUAGE_CODE == "de":
            return f"Am {self.datetime.date[5:]} um {self.datetime.time} werden wir {self.temp:6}{TEMP_UNIT} haben mit einer Luftfeuchtigkeit von {self.humidity:2}% und der Himmel ist zu {self.cloudiness:3}% bewölkt. Es wird zu {self.pop:2.0f}% regnen. --> {self.weather_description}"
        else:
            return f"On the {self.datetime.date[5:]} at {self.datetime.time} will be a temperature of {self.temp:6}{TEMP_UNIT} and a humidity of {self.humidity:2}%, the cloudiness will be {self.cloudiness:3}%. It will rain with a {self.pop:2.0f}% probability. --> {self.weather_description}"


class DailyWeatherData(WeatherData):
    def __repr__(self) -> str:
        if LANGUAGE_CODE == "de":
            return f"Am {self.datetime.date} werden wir zwischen {self.min_temp:6}{TEMP_UNIT} und {self.max_temp:6}{TEMP_UNIT} haben mit einer durchschnitts Luftfeuchtigkeit von {self.humidity:2}% und der Himmel wird zu {self.cloudiness:3}% bewölkt sein. Es wird zu {self.pop:2.0f}% regnen. --> {self.weather_description}"
        else:
            return f"At {self.datetime.date} will be a temperature between {self.min_temp:6}{TEMP_UNIT} and {self.max_temp:6}{TEMP_UNIT} a average humidity of {self.humidity:2}%, the overall cloudiness will be {self.cloudiness:3}%. It will rain with a {self.pop:2.0f}% probability. --> {self.weather_description}"
