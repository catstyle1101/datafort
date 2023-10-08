import json

from pydantic import BaseModel

celsius = float
kelvin = float


class WeatherResponse(BaseModel):
    name: str
    temp: celsius
    temp_max: celsius
    temp_min: celsius
    pressure: int
    humidity: int
    wind_speed: float
    wind_deg: int
    clouds_percent: int
    lat: float
    lon: float


class Coord(BaseModel):
    lon: float
    lat: float


class Weather(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class MainWeather(BaseModel):
    temp: kelvin = None
    feels_like: kelvin = None
    temp_min: kelvin = None
    temp_max: kelvin = None
    pressure: int = None
    humidity: int = None
    sea_level: int = None
    grnd_level: int = None


class Wind(BaseModel):
    speed: float
    deg: int
    gust: float = None


class Clouds(BaseModel):
    all: int


class Sys(BaseModel):
    type: int
    id: int
    country: str
    sunrise: int
    sunset: int


class WeatherOpenWeatherResponse(BaseModel):
    coord: Coord
    weather: list[Weather]
    base: str
    main: MainWeather
    visibility: int
    wind: Wind
    clouds: Clouds
    dt: int
    sys: Sys
    timezone: int
    id: int
    name: str
    cod: int
    rain: dict[str, float] = None
