#This file handles the database connection using SQLAlchemy. It sets up the engine, session, and base declarative class to interact with the PostgreSQL database.

# database.py

from sqlalchemy import create_engine  # Import the function to create a SQLAlchemy engine
from sqlalchemy.ext.declarative import declarative_base  # Import the base class for declarative models
from sqlalchemy.orm import sessionmaker  # Import the sessionmaker function to create a session factory
import os  # Import the os module to access environment variables

# Retrieve the database URL from the environment variable or use a default value
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:mypassword@localhost:5432/pidatabase')

# Create the SQLAlchemy engine that will interface with the PostgreSQL database
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our ORM models
Base = declarative_base()
