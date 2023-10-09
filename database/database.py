import logging
import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .cities import CITIES
from config import CITIES_COUNT
from models import Base, City, Weather
from schemas import WeatherOpenWeatherResponse


class Database(ABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @abstractmethod
    def get_cities(self):
        pass

    @abstractmethod
    def write_weather_to_db(self, weather: WeatherOpenWeatherResponse):
        pass


class SQLite(Database):
    def __init__(self, database_url: str) -> None:
        self.engine = create_engine(database_url, pool_pre_ping=True)
        self.session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        with self.session() as session:
            if not session.query(City).all():
                logging.info('Cities are not in database. Filling...')
                self._fill_database(session)

    def get_cities(self) -> list[City]:
        with self.session() as session:
            results = session.query(City).order_by(
                City.population.desc()).limit(CITIES_COUNT).all()
        return results

    def write_weather_to_db(
            self, weather: WeatherOpenWeatherResponse, city: City) -> None:
        new_weather = Weather(
            id=str(uuid.uuid4()),
            temperature=weather.main.temp,
            weather=weather.weather[0].main,
            weather_description=weather.weather[0].description,
            pressure=weather.main.pressure,
            humidity=weather.main.humidity,
            wind_speed=weather.wind.speed,
            wind_direction=weather.wind.deg,
            clouds=weather.clouds.all,
            city_id=city.id,
            created_at=datetime.utcnow(),
        )
        with self.session() as session:
            session.add(new_weather)
            session.commit()
        logging.info(f'Weather in {city.name} is saved')

    def _fill_database(self, session: Session) -> None:
        Base.metadata.create_all(self.engine)
        with session:
            for name, lat, lon, population in CITIES:
                new_city = City(
                    name=name,
                    lat=lat,
                    lon=lon,
                    population=population,
                    id=str(uuid.uuid4())
                )
                session.add(new_city)
                session.commit()
        logging.info(f'Filled {len(CITIES)} cities to db.')
