from config import DATABASE_URL
from sqlalchemy.engine import create_engine

engine = create_engine(DATABASE_URL)
