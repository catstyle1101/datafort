import logging
import os

db_user = os.environ.get('PGUSER', 'postgres')
db_password = os.environ.get('POSTGRES_PASSWORD', 'postgres')
db_host = os.environ.get('DB_HOST', 'db')
db_port = os.environ.get('DB_PORT', '5432')
db_name = os.environ.get('POSTGRES_DB', 'database')
DATABASE_URL = (
    f'postgresql+psycopg2://{db_user}:{db_password}@'
    f'{db_host}:{db_port}/{db_name}'
)
API_KEY = os.environ.get('OPENWEATHER_API_KEY')
CITIES_COUNT = 50
LOGGING_FORMAT = '%(levelname)s: %(message)s'
LOGGING_LEVEL = logging.INFO
CHUNK_SIZE = 8
