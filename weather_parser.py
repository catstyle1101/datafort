import logging

from celery_config import app
from config import DATABASE_URL, LOGGING_FORMAT
from database import SQLite
from schemas import WeatherOpenWeatherResponse
from session import RequestsSession
from weather_api_service import OpenWeatherParser


@app.task(name='weather_parser.parse_weather')
def parse_weather():
    logging.basicConfig(format=LOGGING_FORMAT)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    db = SQLite(DATABASE_URL)
    cities = db.get_cities()
    session = RequestsSession()
    for city in cities:
        parser = OpenWeatherParser(session=session)
        weather = WeatherOpenWeatherResponse(
            **parser.parse_api(lat=city.lat, lon=city.lon))
        db.write_weather_to_db(weather=weather, city=city)
    logging.info(
        'Information gathered. Pause on: 1 hour'
    )
