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
    return {'google site text': algorithm.extractText("https://www.google.com/")}

