from sqlalchemy import create_engine

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

conn = engine.connect()