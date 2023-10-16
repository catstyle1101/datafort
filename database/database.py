import csv
import logging
import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import CITIES_COUNT, CHUNK_SIZE
from models import Base, City, Weather
from schemas import WeatherOpenWeatherResponse


class BaseModelRepository(ABC):
    """
    Abstract base repository contract for interacting with database models.

    This class defines the interface for repository classes that interact
        with database models.

    """
    @abstractmethod
    def get_all(self):
        """
        Retrieve all records from the associated database table.

        Returns:
            list: A list of records from the database table.
        """
        pass

    @abstractmethod
    def write_one(self, obj):
        """
        Retrieve all records from the associated database table.

        Returns:
            list: A list of records from the database table.
        """
        pass


class TableMaker:
    """
    A utility class for creating database tables based on SQLAlchemy models.

    Args:
        database_url (str): The URL of the database where tables
            will be created.
        base (declarative_base): The declarative base instance
            containing model definitions.
    """
    def __init__(self, datbase_url: str, base: Base):
        """
        Initialize the TableMaker.

        Args:
            database_url (str): The URL of the database where
                tables will be created.
            base (declarative_base): The declarative base instance
                containing model definitions.
        """
        self.engine = create_engine(datbase_url)
        self.base = base

    def create_tables(self):
        """
        Create database tables based on the provided SQLAlchemy models.
        """
        self.base.metadata.create_all(self.engine)


class Database:
    """Create database session and engine in object."""
    def __init__(self, database_url: str) -> None:
        self.engine = create_engine(database_url, pool_pre_ping=True)
        self.session = sessionmaker(bind=self.engine)


class CityRepository(Database, BaseModelRepository):
    """Repository for interacting with City objects in the database."""

    def get_all(self) -> list[City]:
        """
        Get a list of all cities in the database, ordered by population in
        descending order.

        Returns:
            list[City]: A list of City objects.
        """
        with self.session() as session:
            results = session.query(City).order_by(
                City.population.desc()).limit(CITIES_COUNT).all()
        return results

    def write_one(self, city: City) -> None:
        """
        Write a single city to the database.

        Args:
            city (City): The City object to be written to the database.
        """
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
        """
        Fill the database with cities from a predefined list by chunks.

        Note:
            This method is used to populate the database with cities.

        Raises:
            Exception: An error occurred if there was a problem adding a city.
        """
        with open('cities.csv', 'r') as f:
            reader = csv.DictReader(f)
            chunk = []
            for city in reader:
                chunk.append(City(**city, id=str(uuid.uuid4())))
                if len(chunk) >= CHUNK_SIZE:
                    with self.session() as session:
                        session.add_all(chunk)
                        session.commit()
                    chunk = []
            if chunk:
                with self.session() as session:
                    session.add_all(chunk)
                    session.commit()
        logging.info('Filled cities to db.')


class WeatherRepository(Database, BaseModelRepository):
    """Repository for interacting with Weather objects in the database."""

    def get_all(self, city: City) -> list[Weather]:
        """
        Get a list of all weather of city in the database,
        ordered by population in descending order.

        Args:
            city (City): The City object to be written to the database.

        Returns:
            list[Weather]: A list of Weather objects.
        """
        with self.session() as session:
            results = session.query(Weather).where(city_id=city.id).order_by(
                Weather.created_at.desc()).all()
        return results

    def write_one(
            self, weather: WeatherOpenWeatherResponse, city: City) -> None:
        """
        Write a single weather to the database.

        Args:
            weather (WeatherOpenWeatherResponse): The Weather object.
            city (City): The City object to be written to the database.
        """
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
