import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class City(Base):
    __tablename__ = 'cities'

    id = Column(
        String,
        primary_key=True,
        default=str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    name = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    population = Column(Integer)
    weather = relationship('Weather', back_populates='city')

    def __repr__(self):
        return (
            f'{self.name}: population({self.population}), '
            f'(lat={self.lat}, lon={self.lon})'
        )


class Weather(Base):
    __tablename__ = 'weather'

    id = Column(
        String,
        primary_key=True,
        default=str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    temperature = Column(Float)
    weather = Column(String)
    weather_description = Column(String)
    pressure = Column(Integer)
    humidity = Column(Integer)
    wind_speed = Column(Float)
    wind_direction = Column(Float)
    clouds = Column(Integer)
    city_id = Column(String, ForeignKey('cities.id'))
    city = relationship('City', back_populates='weather')
    created_at = Column(DateTime, default=datetime.utcnow)
