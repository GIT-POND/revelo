# # creating api 
# from fastapi import APIRouter, status, HTTPException, Depends
# from pydantic import BaseModel
# from typing import List # for returning lists using schemas

# # creating db session
# from sqlalchemy.orm import Session

# # create SQLALCHEMY models on startup
# from .database import  get_db

# # use webscrape algo
# from .algorithm import search_webpage

# # Replace app with router to app
# router = APIRouter()