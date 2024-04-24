import os

from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine

# get postgres creds from environment - set by Docker compose
DB_USER = os.getenv("PGUSER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOSTNAME = os.getenv("DB_HOSTNAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME if DB_HOSTNAME else 'localhost'}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
