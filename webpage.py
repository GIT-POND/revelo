# creating api 
from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import BaseModel
from typing import List # for returning lists using schemas

# creating db session
from sqlalchemy.orm import Session

# create SQLALCHEMY models on startup
from database import  get_db

# use webscrape algo
import algorithm

# Replace app with router to app
router = APIRouter()


'''
---------------------------------------
            WEBPAGE SEARCH 
---------------------------------------
'''

class ApiIn(BaseModel):
    url: str
class ApiOut(BaseModel):
    hasMisdirection: bool
    hasHiddenAds: bool
    hasForcedCont: bool
    hasFriendSpam: bool
    hasHiddenCosts: bool


@router.get("/model_init")
async def model_init():
    algorithm.create_dataset_from_url('dataset(training).csv', "https://www.microcenter.com/search/search_results.aspx?N=4294966937&Ntk=all&sortby=match&myStore=true")
    algorithm.label_dataset()
    return {'message':'model initialized'}

@router.post("/model_run")
async def model_run(site_data:ApiIn, db: Session = Depends(get_db)):
    algorithm.create_dataset_from_url('dataset(testing).csv', "https://www.microcenter.com/product/638567/msi-nvidia-geforce-rtx-3070-ti-ventus-3x-overclocked-triple-fan-8gb-gddr6x-pcie-40-graphics-card")
    print(site_data)

    return {'running':str(algorithm.trainModel())}

@router.get("/model_results")
async def model_results(model_data:ApiOut):
    return {'message':'database data'}

