from fastapi import FastAPI
from app.database import Base,engine
from app.user import models
from app.user.router import user_routes


Base.metadata.create_all(bind=engine)

app = FastAPI(title= "Job Portal API")

app.include_router(user_routes)

@app.get("/")
def home():
    return {
        "message" : "Job Portal API is running"
    }