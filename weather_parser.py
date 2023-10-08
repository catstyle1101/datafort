import requests

from config import WEATHER_API_URL, API_KEY
from schemas import WeatherOpenWeatherResponse


lat = 55.154
lon = 61.4291
result_json = requests.get(
    WEATHER_API_URL.format(api_key=API_KEY, lat=lat, lon=lon)).json()

weather = WeatherOpenWeatherResponse(**result_json)
print(weather)
