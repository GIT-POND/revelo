# creating api 
from fastapi import FastAPI

# verifying db connection
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# create SQLALCHEMY models on startup
from .database import engine
from . import models
models.Base.metadata.create_all(bind=engine)

# import endpoint file
import webpage_endpoints


app = FastAPI()

# recurring db connection test
while True:
    try:
        conn = psycopg2.connect(host="", database="", user="", password="", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successful.")
        break
    except:
        print("Database connection failed")
        time.sleep(3) #wait three seconds


# include endpoints in endpoints file
app.include_router(webpage_endpoints.router)

# homepage endpoint
@app.get("/")
async def root():
    return {"message":"home page"}

