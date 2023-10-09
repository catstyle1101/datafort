import json
import logging
from abc import ABC, abstractmethod

from config import API_KEY, WEATHER_API_URL
from errors import APIKeyNotFoundError
from session import RequestsSession


class BaseWeatherParser(ABC):
    def __init__(self, session: RequestsSession):
        self.session = session

    @abstractmethod
    def parse_api(self):
        pass


class OpenWeatherParser(BaseWeatherParser):
    def parse_api(self, lat: float, lon: float) -> dict | None:
        if API_KEY is None:
            logging.error('API KEY is not set in .env file')
            raise APIKeyNotFoundError
        url = WEATHER_API_URL.format(lat=lat, lon=lon, api_key=API_KEY)
        try:
            return self.session.get(url).json()
        except json.JSONDecodeError as e:
            logging.error('Server response invalid')
            raise e
