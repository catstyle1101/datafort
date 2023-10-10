from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field

kelvin = float


class Coord(BaseModel):
    """
    Represents the geographical coordinates (latitude and longitude) of a
        location.

    Attributes:
        lon (float): The longitude of the location.
        lat (float): The latitude of the location.
    """
    lat: Annotated[float, Field(ge=-90, le=90)]
    lon: Annotated[float, Field(ge=-180, le=180)]


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
    main: Annotated[str, Field(max_length=100)]
    description: Annotated[str, Field(max_length=100)]
    icon: Annotated[str, Field(max_length=10)]


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
    temp: Optional[Annotated[kelvin, Field(ge=0, le=400)]] = None
    feels_like: Optional[Annotated[kelvin, Field(ge=0, le=400)]] = None
    temp_min: Optional[Annotated[kelvin, Field(ge=0, le=400)]] = None
    temp_max: Optional[Annotated[kelvin, Field(ge=0, le=400)]] = None
    pressure: Optional[Annotated[int, Field(ge=0, le=1500)]] = None
    humidity: Optional[Annotated[int, Field(ge=0, le=100)]] = None
    sea_level: Optional[Annotated[int, Field(ge=0, le=10000)]] = None
    grnd_level: Optional[Annotated[int, Field(ge=0, le=10000)]] = None


class Wind(BaseModel):
    """
    Represents wind information for a location.

    Attributes:
        speed (float): Wind speed in meters per second (m/s).
        deg (int): Wind direction in degrees.
        gust (Optional[float]): Wind gust speed in meters per second (m/s).
    """
    speed: Annotated[float, Field(ge=0, le=1000)]
    deg: Annotated[float, Field(ge=0, le=360)]
    gust: Optional[Annotated[float, Field(ge=0, le=1000)]] = None


class Clouds(BaseModel):
    """
    Represents cloud cover information for a location.

    Attributes:
        all (int): Cloud cover as a percentage.
    """
    all: Annotated[int, Field(ge=0, le=100)]


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
    country: Optional[Annotated[str, Field(max_length=10)]] = None
    sunrise: Optional[Annotated[int, Field(ge=0)]] = None
    sunset: Optional[Annotated[int, Field(ge=0)]] = None


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
    base: Annotated[str, Field(max_length=100)]
    main: MainWeather
    visibility: Annotated[int, Field(ge=0, le=10000)]
    wind: Wind
    clouds: Clouds
    dt: Annotated[int, Field(ge=0)]
    timezone: int
    id: int
    name: Annotated[str, Field(max_length=100)]
    cod: Annotated[int, Field(ge=0, le=1000)]
    sys: Optional[Sys] = None
    rain: Optional[dict[str, float]] = None
