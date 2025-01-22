from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm#, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..data_base import engine, get_db,schema, db_models as models, utails as utils, oauth2



router = APIRouter()

#Creating the users login path
@router.post("/login", response_model = schema.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)): #schema.UserLogin#
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    


        #Create a token
        access_token = oauth2.create_access_token(data = {"user_id": user.id})
        #return a token
        return{"access_token": access_token, "token_type":"bearer"}
    







