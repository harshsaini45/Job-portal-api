from fastapi import FastAPI
from app.database import Base,engine
from app.user import models
from app.jobs import models
from app.user.router import user_routes
from app.jobs.router import job_routes
from app.recruiter.router import recruiter_routes
from app.applications.router import router as applications_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title= "Job Portal API")

app.include_router(user_routes)
app.include_router(job_routes)
app.include_router(recruiter_routes)
app.include_router(applications_router)

@app.get("/")
def home():
    return {
        "message" : "Job Portal API is running"
    }