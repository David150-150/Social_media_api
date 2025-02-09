import pytest
from jose import jwt
from app import schema
from database import client, session
from app.config import settings



def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    #print(res.json())
    assert res.status_code == 201
    new_user = schema.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"


def test_login_user(client, test_user):
    #res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    print(res.json)
    login_res = schema.Token(**res.json())
    payload = jwt.decode( login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
# This checks for the wrong password
@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('kusi@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 403),
    ('kusi@gmail.com', None, 403)
])


def test_incorrect_login(test_user, client, email, password, status_code):
    #res = client.post("/login", data={"username": test_user['email'], "password": "wrongPassword"})
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid credentials'

    # login_res = schema.Token(**res.json())

    # # Decode the JWT token
    # payload = jwt.decode(
    #     login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    # )
    # user_id: str = payload.get("user_id")

    # # Ensure the user_id matches the created user's ID
    # assert user_id == test_user['id']  # Change to 'user_id' if API returns 'user_id'
    # assert login_res.token_type == "bearer"






# def test_login_user(client, test_user):
#     res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
#     assert res.status_code == 200

#     login_res = schema.Token(**res.json())

#     # Decode the JWT token
#     payload = jwt.decode(
#         login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
#     )
#     user_id: str = payload.get("user_id")

#     # Ensure the user_id matches the created user's ID
#     assert user_id == test_user['id']  # Change to 'user_id' if API returns 'user_id'
#     assert login_res.token_type == "bearer"

# @pytest.mark.parametrize("email, password, status_code", [
#     ('wrongemail@gmail.com', 'password123', 403),
#     ('food@gmail.com', 'wrongpassword', 403),
#     (None, 'password123', 422),
#     ('food@gmail.com', None, 422)
# ])
# def test_incorrect_login(client, email, password, status_code):
#     # Ensure None values are properly omitted
#     login_data = {}
#     if email is not None:
#         login_data["username"] = email
#     if password is not None:
#         login_data["password"] = password
    
#     res = client.post("/login", data=login_data)
    
#     assert res.status_code == status_code, f"Expected {status_code}, got {res.status_code}. Response: {res.json()}"
    
#     if status_code == 403:
#         # Case-insensitive check
#         assert res.json().get('detail').lower() == 'invalid credentials'









