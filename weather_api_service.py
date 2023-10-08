from abc import ABC, abstractmethod
import json
import logging

from config import API_KEY, WEATHER_API_URL
from session import RequestSession


class BaseWeatherParser(ABC):
    def __init__(self, session: RequestSession):
        self.session = session

    @abstractmethod
    def parse_api(self):
        pass


class OpenWeatherParser(BaseWeatherParser):
    def parse_api(self, lat: float, lon: float) -> dict | None:
        url = WEATHER_API_URL.format(lat=lat, lon=lon, api_key=API_KEY)
        try:
            return self.session.get(url).json()
        except json.JSONDecodeError:
            logging.error('Server response invalid')
