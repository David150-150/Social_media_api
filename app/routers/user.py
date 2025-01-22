from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import db_models as models, schema, utail as utils
from ..data_base import engine, get_db

#This a Router instance
router = APIRouter(
    prefix="/users",
    tags = ["Users"]
) 

#Route for User
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schema.UserOut)
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    #Hashing the Users password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password


    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#Setting a route that will fetch the  ID depending on the front end
@router.get("/{id}", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    return user
    

    

