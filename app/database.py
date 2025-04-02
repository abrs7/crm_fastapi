import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import time
load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
retries = 5
while retries:
    try:
        engine = create_engine(DATABASE_URL)
        engine.connect()
        break
    except OperationalError:
        retries -= 1
        time.sleep(5)

# engine = create_engine(DATABASE_URL)
if not engine:
    raise RuntimeError("Failed to connect to the database after multiple attempts.")
SessionLocal = sessionmaker(autoflush=False, autocommit= False, bind=engine)

Base = declarative_base()