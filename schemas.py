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
    type: int = None
    id: int = None
    country: str = None
    sunrise: int = None
    sunset: int = None


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
    sys: Sys = None
    rain: dict[str, float] = None
