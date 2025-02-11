
# Import database models from the current package
from . import db_models as models  

# Import necessary SQLAlchemy modules for database connection and ORM handling
from sqlalchemy import create_engine  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker  

# Import the Settings class to access environment variables
from .config import Settings  

# Create an instance of the Settings class to access database configurations
settings = Settings()  

# Construct the database connection URL dynamically using values from settings
DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# Create the SQLAlchemy engine using the constructed DATABASE_URL
engine = create_engine(DATABASE_URL)  

# Configure a session factory that will create new database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  

# Create a base class for defining database models using SQLAlchemy ORM
Base = declarative_base()  

# Dependency function to create and close a database session
def get_db():
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Yield the session for use in request handlers
    finally:
        db.close()  # Ensure the session is closed after the request is handled


