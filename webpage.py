# creating api 
from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import BaseModel
from typing import List,Optional # for returning lists using schemas

# creating db session
from sqlalchemy.orm import Session

# create SQLALCHEMY models on startup
from database import get_db
import models

# use webscrape algo
import algorithm_v2

from datetime import datetime

# Replace app with router to app
router = APIRouter()


'''
---------------------------------------
            SCHEMAS
---------------------------------------
'''
class EntryBase(BaseModel):
    url: str
    scarcity: bool
    countDown: bool
    socialProof: bool
    
    class Config:
        orm_mode = True

class Entry_create(EntryBase):
    date: datetime

class Entry_search(BaseModel):
    url: str

class Entry_reponse(EntryBase):
    pass
    

'''
---------------------------------------
Return searches using URL (if any)
---------------------------------------
'''
@router.get("/search", response_model = Entry_create)
async def model_results(entry:Entry_search,db: Session = Depends(get_db)):
    result = db.query(models.Entry).filter(models.Entry.url == entry.url).first()
    if result is None:
        return {"url":"None","scarcity":False,"countDown":False,"socialProof":False}
    else:
        return result

'''
---------------------------------------
Create searches using URL (if none)
---------------------------------------
'''
@router.post("/process", response_model = Entry_create)
async def model_run(entry:Entry_search, db: Session = Depends(get_db)):

    result = db.query(models.Entry).filter(models.Entry.url == entry.url).first()

    if result is None:
        algorithm_v2.create_dataset('dataset.txt', entry.url)
        results = algorithm_v2.validate_dataset('dataset.txt')

        db_entry = models.Entry(
            url=entry.url, 
            date=datetime.now(), 
            scarcity=True if(results[0]>0)else False, 
            countDown=True if(results[1]>0)else False, 
            socialProof=True if(results[2]>0)else False,
            )
        
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        return db_entry
    else:
        raise HTTPException(status_code=500, detail="URL already used")



'''
Test site 
#https://www.microcenter.com/search/search_results.aspx?N=4294966937&Ntk=all&sortby=match&myStore=true
    
'''