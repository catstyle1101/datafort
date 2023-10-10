from abc import ABC, abstractmethod
import json
import logging
from requests import Session


class BaseWeatherParser(ABC):
    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def parse_api(self):
        pass


class OpenWeatherParser(BaseWeatherParser):
    WEATHER_API_URL = (
        'https://api.openweathermap.org/data/2.5/weather?'
        'lat={lat}&lon={lon}&appid={api_key}'
    )

    def parse_api(self, api_key: str, lat: float, lon: float) -> dict | None:
        url = self.WEATHER_API_URL.format(lat=lat, lon=lon, api_key=api_key)
        logging.debug(url)
        try:
            return self.session.get(url).json()
        except json.JSONDecodeError as e:
            logging.error('Server response invalid')
            raise e
