import os

import requests

# Read the OpenWeatherMap key from the environment instead of hard-coding it.
# Set it before running:  export OPENWEATHER_API_KEY="your-key"
API_KEY = os.environ.get("OPENWEATHER_API_KEY")


def get_weather(lat, lon):
    if not API_KEY:
        raise RuntimeError(
            "OPENWEATHER_API_KEY is not set. Get a free key at "
            "https://openweathermap.org/api and export it as an environment variable."
        )

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"}

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]

    rainfall = 0
    if "rain" in data:
        rainfall = data["rain"].get("1h", 0)

    return {
        "temperature": temperature,
        "humidity": humidity,
        "rainfall": rainfall,
    }
