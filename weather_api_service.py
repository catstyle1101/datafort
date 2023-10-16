from abc import ABC, abstractmethod
import json
import logging
from requests import Session

from errors import ClientError, ServerError


class BaseWeatherParser(ABC):
    """
    Abstract base class for weather data parsers.

    Attributes:
        session (Session): The HTTP session used for making API requests.

    """
    def __init__(self, session: Session):
        """
        Initialize a BaseWeatherParser.

        Args:
            session (Session): The HTTP session used for making API requests.
        """
        self.session = session

    @abstractmethod
    def parse_api(self):
        """
        Abstract method to parse weather data from an API.

        This method should be implemented by subclasses to parse weather data
        from a specific weather API.

        Returns:
            dict | None: A dictionary containing weather data, or None
            if parsing fails.

        """
        pass


class OpenWeatherParser(BaseWeatherParser):
    """
    Weather data parser for the OpenWeatherMap API.

    Attributes:
        WEATHER_API_URL (str): The base URL for the OpenWeatherMap API.

    """

    WEATHER_API_URL = (
        'https://api.openweathermap.org/data/2.5/weather?'
        'lat={lat}&lon={lon}&appid={api_key}'
    )

    def parse_api(self, api_key: str, lat: float, lon: float):
        """
        Parse weather data from the OpenWeatherMap API.

        Args:
            api_key (str): The API key for accessing the OpenWeatherMap API.
            lat (float): The latitude of the location.
            lon (float): The longitude of the location.
        """

        url = self.WEATHER_API_URL.format(lat=lat, lon=lon, api_key=api_key)
        logging.debug(url)
        try:
            result = self.session.get(url)
            if 400 <= result.status_code < 500:
                raise ClientError(result)
            if 500 <= result.status_code < 600:
                raise ServerError(result)
            return result.json()
        except json.JSONDecodeError as e:
            logging.error('Server response invalid')
            raise e
