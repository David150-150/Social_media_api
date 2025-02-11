

# Import necessary modules from Pydantic for schema validation
from pydantic import BaseModel, EmailStr  

# Import datetime for handling timestamps
from datetime import datetime  

# Import Optional for optional fields
from typing import Optional  

# Import conint for constrained integer types
from pydantic.types import conint  

# Import Enum for defining vote directions
from enum import Enum  


# Defines the base structure of a Post request
class PostBase(BaseModel):  
    title: str  # The title of the post (required)
    content: str  # The main content of the post (required)
    publish: bool = True  # Determines if the post is published (default: True)


# Schema for creating a new post, inherits from PostBase
class PostCreate(PostBase):  
    pass  # No additional fields needed beyond PostBase


# Schema for user output (excluding sensitive data like password)
class UserOut(BaseModel):  
    id: int  # Unique user ID
    email: EmailStr  # User email, validated as a proper email format

    class Config:
        from_attributes = True  # Enables ORM model compatibility


# Schema for sending post data back to the user
class Post(PostBase):  
    id: int  # Unique post ID
    created_at: datetime  # Timestamp when the post was created
    owner_id: int  # ID of the user who created the post
    owner: UserOut  # Relationship to the post's owner (UserOut schema)

    class Config:
        from_attributes = True  # Enables compatibility with SQLAlchemy ORM models


# Schema for returning post details along with the number of votes
class PostOut(BaseModel):  
    post: Post  # The actual post details (nested schema)
    votes: int  # Number of votes the post has received

    class Config:
        from_attributes = True  # Enables ORM support


# Schema for creating a new user
class UserCreate(BaseModel):  
    email: EmailStr  # User's email (validated format)
    password: str  # User's password (stored securely in the database)


# Schema for handling user login requests
class UserLogin(BaseModel):  
    email: EmailStr  # Email for authentication
    password: str  # Password for authentication


# Schema for JWT authentication tokens
class Token(BaseModel):  
    access_token: str  # The access token string
    token_type: str  # The type of token (e.g., "bearer")


# Schema for extracting user ID from JWT tokens
class TokenData(BaseModel):  
    id: str  # The user ID extracted from the token


# Enum class defining allowed vote directions
class DirectionEnum(Enum):  
    upvote = 1  # Represents an upvote (value: 1)
    downvote = -1  # Represents a downvote (value: -1)


# Schema for handling vote requests
class Vote(BaseModel):  
    post_id: int  # ID of the post being voted on
    dir: DirectionEnum  # Restrict vote direction to `upvote` or `downvote`
