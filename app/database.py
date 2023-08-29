print(f"app/database.py package: {__package__}")

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import app_settings
SQLALCHEMY_DATABASE_URL = f"postgresql://{app_settings.database_username}:{app_settings.database_password}@{app_settings.database_hostname}:{app_settings.database_port}/{app_settings.database_name}"

engine = create_engine(url=SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

