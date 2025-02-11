
# Import Base from the database module for defining ORM models
from .data_base import Base

# Import SQLAlchemy modules for defining database columns and relationships
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

# Define the Post model, representing the "posts" table
class Post(Base):  
    __tablename__ = "posts"  # Name of the database table

    # Define the columns in the table
    id = Column(Integer, primary_key=True, nullable=False)  # Unique identifier for each post
    title = Column(String, nullable=False)  # Title of the post
    content = Column(String, nullable=False)  # Content of the post
    publish = Column(Boolean, server_default='FALSE', nullable=False)  # Whether the post is published (default: False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))  # Timestamp of post creation

    # Foreign key linking the post to a user (author)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relationship to fetch the owner details when querying posts
    owner = relationship("User")


# Define the User model, representing the "users" table
class User(Base):
    __tablename__ = "users"  # Name of the database table

    # Define the columns in the table
    id = Column(Integer, primary_key=True, nullable=False)  # Unique identifier for each user
    email = Column(String, nullable=False, unique=True)  # User email (must be unique)
    password = Column(String, nullable=False)  # Hashed password for authentication
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))  # Timestamp of account creation
    phone_number = Column(String)  # Optional phone number field


# Define the Vote model, representing the "votes" table
class Vote(Base):
    __tablename__ = "votes"  # Name of the database table

    # Composite primary key (user_id and post_id together must be unique)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)  # User who voted
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)  # Post that received the vote
