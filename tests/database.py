from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
#from app import schema
from app.config import settings
from app.data_base import get_db
from app.data_base import Base


# Construct the DATABASE_URI using the settings
DATABASE_URI = f"postgresql://postgres:DAVID150@localhost:5432/fastapi"

# Setup the SQLAlchemy engine
engine = create_engine(DATABASE_URI)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # This is exclusive
Base.metadata.create_all(bind=engine)  # Create the database tables


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture
def client(session):
    # Override the get_db dependency to use the session from the fixture
    app.dependency_overrides[get_db] = lambda: session
    yield TestClient(app)


## SINCE EVERYTHING HERE HAS ALREADY BEEN MOVED TO CONFTEST.PY FILE, THIS DB DOESN'T MATTER