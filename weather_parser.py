import logging

from celery_config import app
from config import DATABASE_URL, LOGGING_FORMAT, API_KEY, LOGGING_LEVEL
from database import CityRepository, TableMaker, WeatherRepository
from errors import APIKeyNotFoundError
from requests import Session
from models import Base
from schemas import WeatherOpenWeatherResponse
from weather_api_service import OpenWeatherParser


@app.task(name='weather_parser.parse_weather')
def parse_weather():
    """
    Celery task for parsing weather data from the OpenWeatherMap API and
    storing it in the database.

    This task retrieves a list of cities from the database, fetches weather
    data for each city from the OpenWeatherMap API, and stores the data in
    the database using the appropriate repositories.

    Raises:
        APIKeyNotFoundError: If the API_KEY is not set in the environment
        variables.

    """
    if API_KEY is None:
        logging.error('API KEY is not set in .env file')
        raise APIKeyNotFoundError
    logging.basicConfig(format=LOGGING_FORMAT)
    logger = logging.getLogger()
    logger.setLevel(LOGGING_LEVEL)

    table_maker = TableMaker(DATABASE_URL, Base)
    table_maker.create_tables()

    city_repo = CityRepository(DATABASE_URL)
    weather_repo = WeatherRepository(DATABASE_URL)
    cities = city_repo.get_all()
    if not cities:
        city_repo.fill_database()
        cities = city_repo.get_all()
    for city in cities:
        parser = OpenWeatherParser(session=Session())
        weather = WeatherOpenWeatherResponse(
            **parser.parse_api(api_key=API_KEY, lat=city.lat, lon=city.lon))
        weather_repo.write_one(weather=weather, city=city)
    logging.info(
        'Information gathered. Pause on: 1 hour'
    )


if __name__ == '__main__':
    parse_weather()
