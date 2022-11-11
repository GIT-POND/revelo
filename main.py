# creating api 
from fastapi import FastAPI
from datetime import datetime
now = datetime.now()
# import algorithm

# create SQLALCHEMY models on startup
from database import engine
import models
models.Base.metadata.create_all(bind=engine)

# import endpoint file
import  admin
import webpage


app = FastAPI()


# include endpoints in endpoints file
app.include_router(webpage.router)
#app.include_router(admin.router)

# homepage endpoint
@app.get("/")
async def root():
    return {'enpoint accessed': f'Date={now.strftime("%m/%d/%Y")} Time={now.strftime("%H:%M:%S")}'}

