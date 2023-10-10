import logging
import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .cities import CITIES
from config import CITIES_COUNT
from models import Base, City, Weather
from schemas import WeatherOpenWeatherResponse


class BaseModelRepository(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def write_one(self, obj):
        pass


class TableMaker:
    def __init__(self, datbase_url: str, base: Base):
        self.engine = create_engine(datbase_url)
        self.base = base

    def create_tables(self):
        self.base.metadata.create_all(self.engine)


class Database:
    def __init__(self, database_url: str) -> None:
        self.engine = create_engine(database_url, pool_pre_ping=True)
        self.session = sessionmaker(bind=self.engine)


class CityRepository(Database, BaseModelRepository):
    def get_all(self) -> list[City]:
        with self.session() as session:
            results = session.query(City).order_by(
                City.population.desc()).limit(CITIES_COUNT).all()
        return results

    def write_one(self, city: City) -> None:
        new_city = City(
            name=city.name,
            lat=city.lat,
            lon=city.lon,
            population=city.population,
        )
        with self.session() as session:
            try:
                session.add(new_city)
                session.commit()
            except Exception as e:
                logging.error(f'An error occured: {e}')

        logging.info(f'City {new_city} added.')

    def fill_database(self) -> None:
        """Fill database from cities.py file
        (50 most populated cities in the world).
        """
        with self.session() as session:
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


class WeatherRepository(Database, BaseModelRepository):
    def get_all(self, city: City) -> list[Weather]:
        with self.session() as session:
            results = session.query(Weather).where(city_id=city.id).order_by(
                Weather.created_at.desc()).all()
        return results

    def write_one(
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
