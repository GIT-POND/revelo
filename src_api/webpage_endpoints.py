# creating api 
from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import BaseModel
from typing import List # for returning lists using schemas

# creating db session
from sqlalchemy.orm import Session

# create SQLALCHEMY models on startup
from .database import  get_db

# use webscrape algo
from .algorithm import search_webpage

# Replace app with router to app
router = APIRouter()


'''
---------------------------------------
            WEBPAGE SEARCH 
---------------------------------------
'''
# endpoint schema
class Website_in(BaseModel):
    url: str
class Website_out(BaseModel):
    hasMisdirection: bool
    hasHiddenAds: bool
    hasForcedCont: bool
    hasFriendSpam: bool
    hasHiddenCosts: bool

# endpoint
@router.post("/website")
async def search_website(site_data:Website_in, db: Session = Depends(get_db)):
    search_webpage(site_data.url)
    return {"message":site_data}


