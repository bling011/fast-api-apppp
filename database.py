from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from .env
load_dotenv()

# Get the database URL from environment variable
database_url = os.environ.get("DATABASE_URL")

# Check if it loaded correctly
if not database_url:
    raise ValueError("DATABASE_URL environment variable not set or .env file not found.")

# Create the SQLAlchemy engine
engine = create_engine(database_url, echo=True)

# Create a configured session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the declarative base class
Base = declarative_base()
