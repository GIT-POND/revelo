# creating api 
from fastapi import FastAPI
from src import algorithm

# create SQLALCHEMY models on startup
from src.database import engine
from src import models
models.Base.metadata.create_all(bind=engine)

# import endpoint file
from src import  admin
from src import webpage


app = FastAPI()


# include endpoints in endpoints file
app.include_router(webpage.router)
#app.include_router(admin.router)

# homepage endpoint
@app.get("/")
async def root():
    #return {'google site text': algorithm.extractWorkingDataset("https://us.shein.com/")}
    return {'google site text': algorithm.test_func("https://www.mcafee.com/consumer/en-us/landing-page/direct/sem/mtp-family/desktop/brand-ad.html?csrc=bing&csrcl2=main-ad&cctype=desktop-brand&ccstype=&ccoe=direct&ccoel2=sem&affid=1487&cid=238375&utm_source=bing&utm_medium=paidsearch&utm_campaign=[EN-US][Search][Brand]%20McAfee&utm_content=[brand][exact]%20mcafee&utm_term=mcafee&msclkid=9dd4eaa380211cb22b9f89986e6a6772")}

