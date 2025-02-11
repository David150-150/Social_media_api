

import pytest  # Import pytest for testing
from fastapi.testclient import TestClient  # Import FastAPI's test client
from sqlalchemy import create_engine  # Import SQLAlchemy engine for database connection
from sqlalchemy.orm import sessionmaker  # Import sessionmaker for handling database sessions
from sqlalchemy.ext.declarative import declarative_base  # Import base class for models

# Import the FastAPI app and database settings
from app.main import app  
from app.config import settings  
from app.data_base import get_db, Base  
from app.oauth2 import create_access_token  # Function to generate authentication tokens
from app import db_models as models  # Import database models

# Define the PostgreSQL database connection string
DATABASE_URI = f"postgresql://postgres:DAVID150@localhost:5432/fastapi"

# Create a new SQLAlchemy engine for connecting to the test database
engine = create_engine(DATABASE_URI)

# Create a new session factory for managing database transactions
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Generate the database schema (creates tables based on defined models)
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")  # Define a pytest fixture for database session
def session():
    Base.metadata.drop_all(bind=engine)  # Drop all tables before running each test (clean state)
    Base.metadata.create_all(bind=engine)  # Recreate tables before each test

    db = TestingSessionLocal()  # Create a new database session

    try:
        yield db  # Provide the session to the test
    finally:
        db.rollback()  # Roll back any uncommitted changes
        db.close()  # Close the session

@pytest.fixture  # Define a pytest fixture for FastAPI test client
def client(session):
    app.dependency_overrides[get_db] = lambda: session  # Override database dependency with test session
    yield TestClient(app)  # Provide a FastAPI test client

@pytest.fixture  # Define a fixture to create a test user
def test_user(client):
    user_data = {"email": "kusi@gmail.com", "password": "password123"}  # User credentials
    res = client.post("/users/", json=user_data)  # Send request to create user
    assert res.status_code == 201  # Ensure user creation was successful
    new_user = res.json()  # Convert response to JSON
    new_user['password'] = user_data['password']  # Store raw password for authentication tests
    return new_user  # Return user details

@pytest.fixture  # Define another fixture for a second test user
def test_user2(client):
    user_data = {"email": "kusi20@gmail.com", "password": "password123"}  # Second user credentials
    res = client.post("/users/", json=user_data)  # Send request to create user
    assert res.status_code == 201  # Ensure successful user creation
    new_user = res.json()  # Convert response to JSON
    new_user['password'] = user_data['password']  # Store raw password
    return new_user  # Return user details

@pytest.fixture  # Define a fixture to generate an authentication token for test_user
def token(test_user):
    return create_access_token({"user_id": test_user['id']})  # Generate token using user ID

@pytest.fixture  # Define a fixture for an authenticated test client
def authorized_client(client, token):
    client.headers = {
        **client.headers,  # Keep existing headers
        "Authorization": f"Bearer {token}"  # Add authentication token in headers
    }
    return client  # Return authenticated client

# Function to create a Post model object
def create_post_model(post):
    return models.Post(**post)  # Convert dictionary data into a Post model object

@pytest.fixture()  # Define a fixture to create multiple test posts
def test_posts(test_user, session, test_user2):
    posts_data = [
        {"title": "first title", "content": "first content", "owner_id": test_user['id']},  # Post 1 by test_user
        {"title": "2nd title", "content": "2nd content", "owner_id": test_user['id']},  # Post 2 by test_user
        {"title": "3rd title", "content": "3rd content", "owner_id": test_user['id']},  # Post 3 by test_user
        {"title": "4th title", "content": "4th content", "owner_id": test_user2['id']}  # Post 4 by test_user2
    ]

    posts = [create_post_model(post) for post in posts_data]  # Create Post model objects
    session.add_all(posts)  # Add all posts to the database session
    session.commit()  # Save changes to the database

    return session.query(models.Post).all()  # Return all test posts from the database
