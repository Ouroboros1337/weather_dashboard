LANGUAGE_CODE = "de"
TEMP_UNIT = "°C"
SPEED_UNIT = "m/s"
WEATHER_API_PARAMETERS = {"units": "metric", "lang": LANGUAGE_CODE, "exclude": ""}

with open("./weather_dashboard/api_key.txt", "r") as f:
    WEATHER_API_KEY = f.read()

print(WEATHER_API_KEY)
