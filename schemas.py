from typing import Optional
from pydantic import BaseModel

kelvin = float


class Coord(BaseModel):
    """
    Represents the geographical coordinates (latitude and longitude) of a
        location.

    Attributes:
        lon (float): The longitude of the location.
        lat (float): The latitude of the location.
    """
    lon: float
    lat: float


class Weather(BaseModel):
    """
    Represents weather information for a location.

    Attributes:
        id (int): The weather condition ID.
        main (str): The main weather condition (e.g., 'Clear', 'Rain').
        description (str): A description of the weather conditions.
        icon (str): An icon representing the weather condition.

    """
    id: int
    main: str
    description: str
    icon: str


class MainWeather(BaseModel):
    """
    Represents main weather information for a location.

    Attributes:
        temp (Optional[float]): The temperature in Kelvin (K).
        feels_like (Optional[float]): The "feels like" temperature
            in Kelvin (K).
        temp_min (Optional[float]): The minimum temperature in Kelvin (K).
        temp_max (Optional[float]): The maximum temperature in Kelvin (K).
        pressure (Optional[int]): Atmospheric pressure in hPa (hectopascals).
        humidity (Optional[int]): Relative humidity as a percentage.
        sea_level (Optional[int]): Atmospheric pressure at sea level in hPa.
        grnd_level (Optional[int]): Atmospheric pressure at ground level
            in hPa.
    """
    temp: Optional[kelvin] = None
    feels_like: Optional[kelvin] = None
    temp_min: Optional[kelvin] = None
    temp_max: Optional[kelvin] = None
    pressure: Optional[int] = None
    humidity: Optional[int] = None
    sea_level: Optional[int] = None
    grnd_level: Optional[int] = None


class Wind(BaseModel):
    """
    Represents wind information for a location.

    Attributes:
        speed (float): Wind speed in meters per second (m/s).
        deg (int): Wind direction in degrees.
        gust (Optional[float]): Wind gust speed in meters per second (m/s).
    """
    speed: float
    deg: int
    gust: Optional[float] = None


class Clouds(BaseModel):
    """
    Represents cloud cover information for a location.

    Attributes:
        all (int): Cloud cover as a percentage.
    """
    all: int


class Sys(BaseModel):
    """
    Represents system-related information for a location.

    Attributes:
        type (Optional[int]): System type.
        id (Optional[int]): System ID.
        country (Optional[str]): Country code.
        sunrise (Optional[int]): Sunrise time (Unix timestamp).
        sunset (Optional[int]): Sunset time (Unix timestamp).
    """
    type: Optional[int] = None
    id: Optional[int] = None
    country: Optional[str] = None
    sunrise: Optional[int] = None
    sunset: Optional[int] = None


class WeatherOpenWeatherResponse(BaseModel):
    """
    Represents the response data from the OpenWeather API for weather
    information.

    Attributes:
        coord (Coord): The geographical coordinates of the location.
        weather (List[Weather]): A list of weather conditions for the location.
        base (str): The data source.
        main (MainWeather): Main weather information for the location.
        visibility (int): Visibility in meters.
        wind (Wind): Wind information for the location.
        clouds (Clouds): Cloud cover information for the location.
        dt (int): Time of data calculation (Unix timestamp).
        timezone (int): Timezone offset in seconds from UTC.
        id (int): Location ID.
        name (str): Location name.
        cod (int): Response code.
        sys (Optional[Sys]): System-related information for the location.
        rain (Optional[Dict[str, float]]): Rain information (if available).

    """
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
