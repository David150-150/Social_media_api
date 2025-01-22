from .data_base import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    #Create a table name and defines how the database will look like
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    publish = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))
    
    #This a foreignKey with the user
    owner_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable=False)
    

    owner = relationship("User")
    



#Creating a class for USERs functionality like registration 

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))
    phone_number = Column(String)


#Creating a class for Voting: Composite key takes place here

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)