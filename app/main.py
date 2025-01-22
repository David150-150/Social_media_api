from fastapi import FastAPI                   
from typing import Optional, ClassVar, List                                           
from .routers import post, user, vote #, auth
from .config import Settings

from . import db_models as models, schema, utail as utils #JUST know that naming can affact your code its should have been from . import models
from .data_base import engine#, get_db #no longer need SessionLocal
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

#This allows all web protocoles but you can also be specific like this "[origins = [https://www.youtube.com]....etc]"
origins = ["*"]

# origins = [
#     "http://localhost",  # For local development
#     "http://127.0.0.1",  # For local IP-based testing
#     "http://localhost:8000",  # Specific port
#     "https://localhost:8000"  # Secure local testing
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Include Routers
app.include_router(post.router)
app.include_router(user.router)
#app.include_router(auth.router)
app.include_router(vote.router)














