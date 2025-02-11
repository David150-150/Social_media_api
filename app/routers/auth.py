
from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter  # Import necessary FastAPI modules
from fastapi.security.oauth2 import OAuth2PasswordRequestForm  # Import OAuth2 password form for authentication
from sqlalchemy.orm import Session  # Import Session for database interaction
from ..data_base import get_db, engine  # Import database session dependency
from .. import db_models as models  # Import database models
from .. import schema  # Import schema definitions for request/response validation
from .. import utails as utils  # Import utility functions (likely for password handling)
from .. import oauth2  # Import OAuth2 module for token handling
from ..oauth2 import create_access_token  # Import function to create access tokens

# Define an API router with a prefix and tags for organization
router = APIRouter(prefix="/auth", 
                   tags=["Authentication"])  

router = APIRouter()  

@router.post("/login", response_model=schema.Token)  # Define login route that returns a token response
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),  # Extract login credentials from request
    db: Session = Depends(get_db)  # Inject database session dependency
):
    # Check if user exists in the database using the provided email (username field in OAuth2)
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    # If user is not found, raise an HTTP 403 Forbidden error
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    
    # Verify the provided password against the stored hashed password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    # Generate an access token for the authenticated user
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # Return the generated token in response
    return {"access_token": access_token, "token_type": "bearer"}
