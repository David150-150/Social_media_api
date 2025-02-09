from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated
from . import db_models as db_models, schema, data_base
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import Settings


oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")
settings = Settings()
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes #60  # Consider extending this for production

# Define a function for the Token
def create_access_token(data: dict):
    to_encode = data.copy()  # into our token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Create a function to verify the access token
def verify_access_token(token: str, credential_exception):
    try:
        # Decode the token using the SECRET_KEY and ALGORITHM
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Extract the user ID from the payload
        user_id = str(payload.get("user_id"))

        # If the user ID is missing, raise a credential exception
        if user_id is None:
            raise credential_exception
        token_data = schema.TokenData(id=user_id)

    except JWTError:
        raise credential_exception

    return token_data


#This is to help fetch from the database
def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(data_base.get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token = verify_access_token(token, credential_exception)
    #return await verify_access_token(token, credential_exception)
    user = db.query(db_models.User).filter(db_models.User.id == token.id).first()
    return user
