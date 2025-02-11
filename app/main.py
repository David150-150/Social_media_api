

# Import FastAPI framework for building the API
from fastapi import FastAPI                  

# Import necessary types for type hinting
from typing import Optional, ClassVar, List

# Import database models and utility functions
from . import db_models as db_models, utails as utails                                        

# Import different route modules
from .routers import post, user, vote, auth  

# Import settings configuration
from .config import Settings

# Import schemas (data validation models)
from . import schema  

# Import database engine for table creation
from .data_base import engine 

# Import CORS middleware to handle cross-origin requests
from fastapi.middleware.cors import CORSMiddleware


# Initialize FastAPI application
app = FastAPI()

# Define the allowed origins (currently allowing all domains)
origins = ["*"]

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from any origin (* means all)
    allow_credentials=True,  # Allow credentials (cookies, authorization headers)
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers in requests
)


# Include different routers to organize endpoints
app.include_router(post.router)  # Routes for handling posts
app.include_router(user.router)  # Routes for handling users
app.include_router(auth.router)  # Routes for authentication (login/signup)
app.include_router(vote.router)  # Routes for handling votes (upvotes/downvotes)


# Define the root endpoint
@app.get("/")
def root():
    return {"message": "Hello world!"}  # Returns a simple JSON response
