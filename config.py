import os

DATABASE_URL = 'sqlite+pysqlite:///db/db.sqlite3'
API_KEY = os.environ.get('OPENWEATHER_API_KEY')
CITIES_COUNT = 50
LOGGING_FORMAT = '%(levelname)s: %(message)s'
