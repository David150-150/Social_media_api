    

    

# Import required FastAPI modules
from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
# Import SQLAlchemy session for database interaction
from sqlalchemy.orm import Session

# Import database models and utility functions
from .. import db_models as db_models, utails as utails
# Import schema definitions for request and response validation
from .. import schema
# Import database connection utilities
from ..data_base import engine, get_db

# Create a FastAPI router for user-related operations
router = APIRouter(
    prefix="/users",  # Sets the route prefix to "/users"
    tags=["Users"]  # Categorizes the endpoints under "Users"
) 

# Define an endpoint to create a new user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    # Hash the user's password before storing it
    hashed_password = utails.hash(user.password)
    user.password = hashed_password  # Replace the plain password with the hashed one

    # Create a new user instance using the provided data
    new_user = db_models.User(**user.dict())
    db.add(new_user)  # Add the new user to the database session
    db.commit()  # Save the changes to the database
    db.refresh(new_user)  # Refresh the instance with the latest database state

    return new_user  # Return the created user details

# Define an endpoint to fetch a user by ID
@router.get("/{id}", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    # Query the database to find the user with the given ID
    user = db.query(db_models.User).filter(db_models.User.id == id).first()
    
    # If no user is found, return a 404 error
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # HTTP status for "Not Found"
            detail=f"User with id: {id} not found"  # Error message
        )
    
    return user  # Return the user details
