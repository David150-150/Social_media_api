
# Import necessary libraries for JWT authentication
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated

# Import database models, schemas, and database connection utilities
from . import db_models as db_models, schema, data_base

# Import FastAPI dependencies for authentication and HTTP exceptions
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

# Import SQLAlchemy session handling
from sqlalchemy.orm import Session

# Import settings to retrieve environment variables
from .config import Settings


# Define OAuth2 password bearer token scheme (used for login authentication)
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

# Load application settings from the configuration file
settings = Settings()

# Retrieve security configurations from the settings
SECRET_KEY = settings.secret_key  # Secret key for signing JWTs
ALGORITHM = settings.algorithm  # Algorithm used for encryption
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes  # Token expiration time (in minutes)

# Function to create a JWT access token
def create_access_token(data: dict):
    to_encode = data.copy()  # Create a copy of the data to be encoded
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Set expiration time
    to_encode.update({"exp": expire})  # Add expiration to the token payload
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Encode the token
    return encoded_jwt  # Return the generated JWT token


# Function to verify and decode an access token
def verify_access_token(token: str, credential_exception):
    try:
        # Decode the JWT token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract user ID from the token payload
        user_id = str(payload.get("user_id"))

        # If the token does not contain a valid user ID, raise an exception
        if user_id is None:
            raise credential_exception
        
        # Create a TokenData object containing the extracted user ID
        token_data = schema.TokenData(id=user_id)

    except JWTError:
        # If the token is invalid or tampered with, raise an authentication exception
        raise credential_exception

    return token_data  # Return extracted token data


# Function to retrieve the currently authenticated user from the database
def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(data_base.get_db)):
    # Define an authentication error response in case credentials are invalid
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    # Verify the access token and extract user information
    token = verify_access_token(token, credential_exception)

    # Query the database to retrieve the user associated with the token's user ID
    user = db.query(db_models.User).filter(db_models.User.id == token.id).first()

    return user  # Return the authenticated user object
