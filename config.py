import os


DATABASE_URL = 'sqlite+pysqlite:///db.sqlite3'
API_KEY = os.environ.get('OPENWEATHER_API_KEY')
WEATHER_API_URL = (
    'https://api.openweathermap.org/data/2.5/weather?'
    'lat={lat}&lon={lon}&appid={api_key}'
)
