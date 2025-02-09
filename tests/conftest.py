# from fastapi.testclient import TestClient
# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from app.main import app
# #from app import schema
# from app.config import settings
# from app.data_base import get_db
# from app.data_base import Base
# from app.oauth2 import create_access_token
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Importing the app and database
from app.main import app
from app.config import settings
from app.data_base import get_db, Base

# Import authentication-related functions
from app.oauth2 import create_access_token  # ✅ This is correctly placed
from app import db_models as models



# Construct the DATABASE_URI using the settings
DATABASE_URI = f"postgresql://postgres:DAVID150@localhost:5432/fastapi"

# Setup the SQLAlchemy engine
engine = create_engine(DATABASE_URI)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # This is exclusive
Base.metadata.create_all(bind=engine)  # Create the database tables

# Function to get a database session
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @pytest.fixture(scope="module")
# def session():
#     # Drop and recreate all tables before tests
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     yield db
#     db.close()

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

@pytest.fixture
def test_user2(client):
    user_data = {"email": "kusi20@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    #print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password'] 
    return new_user



@pytest.fixture
def test_user(client):
    user_data = {"email": "kusi@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    #print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password'] 
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

# def create_post_model(post):
#     return models.Post(**post)
#     post_map = map(create_post_model, posts_data)
#     posts = list(post_map)
#     session.add_all(posts)


# #map(create_post_model, posts_data)



# @pytest.fixture()
# def test_posts(test_user, session):#, test_user2):
#     posts_data = [
#         {"title": "first title", "content": "first content", "owner_id": test_user['id']},
#         {"title": "2nd title", "content": "2nd content", "owner_id": test_user['id']},
#         {"title": "3rd title", "content": "3rd content", "owner_id": test_user['id']}

        
#         #{"title": "4th title", "content": "4th content", "owner_id": test_user2['id']}
#     ]

#     # session.add_all([models.Post(title = "first tittle", content = "first content", woner_id =test_user['id']),
#     #                  models.Post(title = "2nd tittle", content = "2nd content", woner_id =test_user['id']),
#     #                  models.Post(title = "3rd tittle", content = "3rd content", woner_id =test_user['id'])])
    
#     session.commit()
#     posts = session.query(models.Post).all()
#     return posts
    

def create_post_model(post):
    return models.Post(**post)  # ✅ Only creates a Post object

@pytest.fixture()
def test_posts(test_user, session, test_user2):
    posts_data = [
        {"title": "first title", "content": "first content", "owner_id": test_user['id']},
        {"title": "2nd title", "content": "2nd content", "owner_id": test_user['id']},
        {"title": "3rd title", "content": "3rd content", "owner_id": test_user['id']},
        {"title": "4th title", "content": "4th content", "owner_id": test_user2['id']}
    ]

    # ✅ Correctly create and insert posts
    posts = [create_post_model(post) for post in posts_data]
    session.add_all(posts)
    session.commit()

    return session.query(models.Post).all() 









# # This is a special file that pytest uses for fixtures
# from fastapi.testclient import TestClient
# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from app.main import app
# from app import schema
# from app.config import settings
# from app.data_base import get_db
# from app.data_base import Base
# from app.oauth2 import create_access_token
# from app import db_models as models







# #settings = Settings()
# #SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:DAVID150@localhost:5432/fastapi_test'
# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

# # Setup the SQLAlchemy engine
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # This is exclusive

# #Base.Base.metadata.create_all(bind=engine)
# #Base = declarative_base()

# # Function to get a database session
# # def override_get_db():
# #     db = TestingSessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()


# #app.dependency_overrides[get_db]=override_get_db




# #client = TestClient(app)

# @pytest.fixture()
# def session():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @pytest.fixture()
# def client( session):
#     #return TestClient(app)
#     #Base.Base.metadata.drop_all(bind=engine)
#     #Base.Base.metadata.create_all(bind=engine)
   
#     def override_get_db():
#     #db = TestingSessionLocal()
#         try:
#             yield session
#         finally:
#             session.close()
#     app.dependency_overrides[get_db]=override_get_db


   
#     yield TestClient(app)
    

# @pytest.fixture
# def test_user2(client):
#     user_data = {"username":"hello20@123.yahoo.com", "password":"DAVID150"}
#     res = client.post("/users/", json= user_data)
#     assert res.status_code == 201
#     print(res.json())
#     new_user = res.json()
#     new_user['password'] = user_data['password']
#     return new_user
    






# @pytest.fixture
# def test_user(client):
#     user_data = {"username":"hello@123.yahoo.com", "password":"DAVID150"}
#     res = client.post("/users/", json= user_data)
#     assert res.status_code == 201
#     print(res.json())
#     new_user = res.json()
#     new_user['password'] = user_data['password']
#     return new_user
    

# @pytest.fixture
# def token(test_user):
#     return create_access_token({"user_id": test_user['id']})

# @pytest.fixture
# def authorized_client(client, token):
#     client.headers = {
#         ** client.headers,
#         "Authorization": f"Bearer {token}"
#     }

#     return client

# # @pytest.fixture
# # def test_posts(test_user, session, test_user2):
# #     posts_data = [{"title": "first tittle",
# #                    "content": "first content",
# #                    "owner_id": "test_user['id']"
# #                    }, {
# #                        "title": "2nd tittle",
# #                    "content": "2nd content",
# #                    "owner_id": "test_user['id']"
# #                    }, {
# #                        "title": "3rd tittle",
# #                    "content": "3rd content",
# #                    "owner_id": "test_user['id']"
# #                    },{
# #                       "title": "3rd tittle",
# #                    "content": "3rd content",
# #                    "owner_id": "test_user2['id']" 
# #                    }]
              
    
# #     def create_post_model(post):
# #         return models.Post(**post)
# #     post_map = map(create_post_model, posts_data)
# #     posts = list(post_map)
# #     session.add_all(posts)


# #     # session.add_all([models.posts(title = "first tittle", content = "first content", woner_id =test_user['id']),
# #     #                  models.posts(title = "2nd tittle", content = "2nd content", woner_id =test_user['id']),
# #     #                  models.posts(title = "3rd tittle", content = "3rd content", woner_id =test_user['id'])])
    
# #     session.commit()
# #     posts = session.query(models.post).all()
# #     return posts
    
                   


# @pytest.fixture()
# def test_posts(test_user, session, test_user2):
#     posts_data = [
#         {"title": "first title", "content": "first content", "owner_id": test_user['id']},
#         {"title": "2nd title", "content": "2nd content", "owner_id": test_user['id']},
#         {"title": "3rd title", "content": "3rd content", "owner_id": test_user['id']},
#         {"title": "4th title", "content": "4th content", "owner_id": test_user2['id']}
#     ]

#     def create_post_model(post):
#         return models.Post(**post)
    
#     post_map = map(create_post_model, posts_data)
#     posts = list(post_map)
#     session.add_all(posts)
#     session.commit()
    
#     posts = session.query(models.Post).all()
#     return posts



# from fastapi.testclient import TestClient
# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from app.main import app
# from app import schema
# from app.config import settings
# from app.data_base import get_db
# from app.data_base import Base
# from app.oauth2 import create_access_token
# from app import db_models as models

# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

# # Setup the SQLAlchemy engine
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# @pytest.fixture()
# def session():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @pytest.fixture()
# def client(session):
#     # Override get_db to use the test session
#     def override_get_db():
#         try:
#             yield session
#         finally:
#             session.close()
    
#     app.dependency_overrides[get_db] = override_get_db
#     yield TestClient(app)


# @pytest.fixture()
# def test_user(client):
#     user_data = {"username": "hello@123.yahoo.com", "password": "DAVID150"}
#     res = client.post("/users/", json=user_data)
    
#     # Print response for debugging
#     print(res.json())  # Debugging output to capture error details

#     # Handle possible error response
#     if res.status_code == 422:
#         raise ValueError(f"Validation Error: {res.json()}")
    
#     assert res.status_code == 201
#     new_user = res.json()
#     new_user['password'] = user_data['password']  # Store original password
#     return new_user
# @pytest.fixture()
# def test_user(client):
#     user_data = {
#         "email": "hello@123.yahoo.com",  # Change from "username" to "email"
#         "password": "DAVID150"
#     }
#     res = client.post("/users/", json=user_data)
    
#     print(res.json())  # Debugging output to capture error details

#     if res.status_code == 422:
#         raise ValueError(f"Validation Error: {res.json()}")
    
#     assert res.status_code == 201
#     new_user = res.json()
#     return new_user









# @pytest.fixture()
# def authorized_client(client, test_user):
#     #response = client.post("/login", data={"username": test_user.username, "password": test_user.password})
#     response = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
#     access_token = response.json().get("access_token")
#     headers = {"Authorization": f"Bearer {access_token}"}
#     return client, headers


# @pytest.fixture()
# def test_user(client):
#     user_data = {
#         "email": "hello@123.yahoo.com",
#         "password": "DAVID150"
#     }
#     res = client.post("/users/", json=user_data)
#     assert res.status_code == 201
    
#     new_user = res.json()
#     new_user["password"] = user_data["password"]  # Store plaintext password for login test
#     return new_user


# @pytest.fixture()
# def test_user2(client):
#     user_data = {
#         "email": "hello20@123.yahoo.com",  # Ensure only the email is provided
#         "password": "DAVID150"
#     }
#     #user_data = {"username": "hello20@123.yahoo.com", "email": "hello20@123.yahoo.com", "password": "DAVID150"}
#     res = client.post("/users/", json=user_data)
    
#     # Print response for debugging
#     print(res.json())  # Debugging output to capture error details

#     if res.status_code == 422:
#         raise ValueError(f"Validation Error: {res.json()}")
    
#     assert res.status_code == 201
#     new_user = res.json()
#     new_user['password'] = user_data['password']
#     return new_user


# @pytest.fixture()
# def test_posts(test_user, session, test_user2):
#     posts_data = [
#         {"title": "first title", "content": "first content", "owner_id": test_user['id']},
#         {"title": "2nd title", "content": "2nd content", "owner_id": test_user['id']},
#         {"title": "3rd title", "content": "3rd content", "owner_id": test_user['id']},
#         {"title": "4th title", "content": "4th content", "owner_id": test_user2['id']}
#     ]

#     def create_post_model(post):
#         return models.Post(**post)
    
#     post_map = map(create_post_model, posts_data)
#     posts = list(post_map)
#     session.add_all(posts)
#     session.commit()
    
#     posts = session.query(models.Post).all()
#     return posts


