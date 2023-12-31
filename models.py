import uuid
from datetime import datetime

from sqlalchemy import (
    Column, DateTime, Float, Enum, ForeignKey, Integer, String)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class City(Base):
    """
    Represents a city with associated weather data.

    Attributes:
        id (uuid4): A unique identifier for the city.
        name (str): The name of the city.
        lat (float): The latitude of the city's location.
        lon (float): The longitude of the city's location.
        population (int): The population of the city.
        weather (relationship): A one-to-many relationship with weather
            records.

    Methods:
        validate(): Validates the integrity of city attributes.
        __repr__(): Returns a string representation of the city.

    """
    __tablename__ = 'cities'

    id = Column(
        String,
        primary_key=True,
        default=str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    name = Column(String(100))
    lat = Column(Float(decimal_return_scale=6, precision=10))
    lon = Column(Float(decimal_return_scale=6, precision=9))
    population = Column(Integer)
    weather = relationship('Weather', backref='city')

    def validate(self):
        if not -180 <= self.lat <= 180:
            raise ValueError('Latitude must be from -180 and 180')
        if not -90 <= self.lon <= 90:
            raise ValueError('Longitude must be from -90 to 90')
        if self.population < 0:
            raise ValueError('Population must be over 0')

    def __repr__(self):
        return (
            f'{self.name}: population({self.population}), '
            f'(lat={self.lat}, lon={self.lon})'
        )


class Weather(Base):
    """
    Represents weather data for a specific city at a particular time.

    Attributes:
        id (uuid4): A unique identifier for the weather record.
        temperature (float): The temperature in degrees Kelvin.
        weather (str): The weather condition (e.g., 'Rain', 'Clear').
        weather_description (str): A description of the weather conditions.
        pressure (int): Atmospheric pressure in hPa (hectopascals).
        humidity (int): Relative humidity as a percentage.
        wind_speed (float): Wind speed in meters per second.
        wind_direction (float): Wind direction in degrees.
        clouds (int): Cloud cover in percentage.
        created_at (datetime): The timestamp when the weather record was
            created.
        city_id (str): The identifier of the associated city.

    Methods:
        validate(): Validates the integrity of weather data attributes.
    """
    __tablename__ = 'weather'

    id = Column(
        String,
        primary_key=True,
        default=str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    temperature = Column(Float(precision=6, decimal_return_scale=2))
    weather = Column(Enum(
        'Thunderstorm', 'Drizzle', 'Rain', 'Snow', 'Mist', 'Smoke', 'Haze',
        'Dust', 'Fog', 'Sand', 'Ash', 'Squall', 'Tornado', 'Clear', 'Clouds',
        name='weather_enum'
    ))
    weather_description = Column(String(100))
    pressure = Column(Integer)
    humidity = Column(Integer)
    wind_speed = Column(Float)
    wind_direction = Column(Float)
    clouds = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    city_id = Column(String, ForeignKey('cities.id'))

    def validate(self):
        if not 0 < self.pressure <= 1500:
            raise ValueError('Pressure must be from 0 to 1500')
        if not self.wind_speed >= 0:
            raise ValueError('Wind speed must be positive')
        if not 0 >= self.wind_direction >= 360:
            raise ValueError('Wind direction must be from 0 to 360')
        if not 0 >= self.humidity >= 100:
            raise ValueError('Humidity must be from 0 to 100')
