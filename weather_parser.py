import logging

from celery_config import app
from config import DATABASE_URL, LOGGING_FORMAT, API_KEY
from database import CityRepository, TableMaker, WeatherRepository
from errors import APIKeyNotFoundError
from requests import Session
from models import Base
from schemas import WeatherOpenWeatherResponse
from weather_api_service import OpenWeatherParser


@app.task(name='weather_parser.parse_weather')
def parse_weather():
    if API_KEY is None:
        logging.error('API KEY is not set in .env file')
        raise APIKeyNotFoundError
    logging.basicConfig(format=LOGGING_FORMAT)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

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
