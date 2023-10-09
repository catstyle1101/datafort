from typing import Optional
from pydantic import BaseModel

kelvin = float


class Coord(BaseModel):
    lon: float
    lat: float


class Weather(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class MainWeather(BaseModel):
    temp: Optional[kelvin] = None
    feels_like: Optional[kelvin] = None
    temp_min: Optional[kelvin] = None
    temp_max: Optional[kelvin] = None
    pressure: Optional[int] = None
    humidity: Optional[int] = None
    sea_level: Optional[int] = None
    grnd_level: Optional[int] = None


class Wind(BaseModel):
    speed: float
    deg: int
    gust: Optional[float] = None


class Clouds(BaseModel):
    all: int


class Sys(BaseModel):
    type: Optional[int] = None
    id: Optional[int] = None
    country: Optional[str] = None
    sunrise: Optional[int] = None
    sunset: Optional[int] = None


class WeatherOpenWeatherResponse(BaseModel):
    coord: Coord
    weather: list[Weather]
    base: str
    main: MainWeather
    visibility: int
    wind: Wind
    clouds: Clouds
    dt: int
    timezone: int
    id: int
    name: str
    cod: int
    sys: Optional[Sys] = None
    rain: Optional[dict[str, float]] = None
