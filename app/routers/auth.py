# from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm#, OAuth2PasswordBearer
# from sqlalchemy.orm import Session
# #from ..data_base import engine, get_db,schema, db_models as models, utails as utils, oauth2
# from ..data_base import engine, get_db, db_models as models, utails as utils, oauth2
# from .. import schema  # Correct way to import schema

# from ..oauth2 import create_access_token

# # app/routers/auth.py
from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..data_base import get_db, engine  # Keep only what’s necessary
from .. import db_models as models  # Only import db_models here, not the entire data_base
from .. import schema  # Import schema here
from .. import utails as utils
from .. import oauth2
from ..oauth2 import create_access_token


router = APIRouter(prefix="/auth", tags=["Authentication"])


router = APIRouter()

#Creating the users login path
# @router.post("/login", response_model = schema.Token)
# async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)): #schema.UserLogin#
#     user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid credentials")
    
#     if not utils.verify(user_credentials.password, user.password):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    


#         #Create a token
#         access_token = oauth2.create_access_token(data = {"user_id": user.id})
#         #return a token
#         return{"access_token": access_token, "token_type":"bearer"}
    

@router.post("/login", response_model=schema.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # Check if user exists by email
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    # If no user is found, raise an Unauthorized (403) exception
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,  # Changed to 403 for invalid credentials
            detail="Invalid credentials"
        )
    
    # Verify password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,  # Changed to 403 for invalid credentials
            detail="Invalid credentials"
        )

    # Create access token if credentials are valid
    # access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    # # Return the token
    # return {"access_token": access_token, "token_type": "bearer"}

    access_token = oauth2.create_access_token(data={"user_id": user.id})

# Return the token
    return {"access_token": access_token, "token_type": "bearer"}

