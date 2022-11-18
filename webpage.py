# creating api 
from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import BaseModel
from typing import List # for returning lists using schemas

# creating db session
from sqlalchemy.orm import Session

# create SQLALCHEMY models on startup
from database import get_db
import models

# use webscrape algo
import algorithm_v2

# Replace app with router to app
router = APIRouter()

import datetime as dt


'''
---------------------------------------
            SCHEMAS
---------------------------------------
'''
class WebpageCreate(BaseModel):
    url: str
class SearchCreate(BaseModel):
    scarcity: bool
    countDown: bool
    socialProof: bool
class SearchReturn(BaseModel):
    scarcity: bool
    countDown: bool
    socialProof: bool
    
    orm_mode = True

'''
---------------------------------------
Return searches using URL (if any)
---------------------------------------
'''
@router.get("/lookup_webpage")
async def model_results(input:WebpageCreate,db: Session = Depends(get_db)):
    result = db.query(models.Webpage).filter(models.Webpage.url == input.url).first()
    return {'message':result}

'''
---------------------------------------
Create searches using URL (if none)
---------------------------------------
'''
@router.post("/scrape_webpage")
async def model_run(input:WebpageCreate, db: Session = Depends(get_db)):
    
    #TODO: register webpage using models.Webpage
    
    #TODO: create searches associated to the webpage
    algorithm_v2.create_dataset('dataset(testing).csv', input.url)
    results = algorithm_v2.validate_dataset
    entry = models.Search(date = dt.now(), scarcity=results[0], countDown=results[1], socialProof=results[2])
    #db.add(entry)
    #db.commit()
    #db.refresh(entry)
    return {entry}


'''
Test site 
#https://www.microcenter.com/search/search_results.aspx?N=4294966937&Ntk=all&sortby=match&myStore=true
    
'''