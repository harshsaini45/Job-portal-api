from fastapi import APIRouter,Depends,Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.jobs import controller
from app.recruiter import controller as recruiter_controller
from app.recruiter.models import RecruiterModel
from app.jobs.dtos import JobSchema,JobUpdateSchema
from app.jobs.models import JobModel


job_routes = APIRouter(prefix="/jobs")

@job_routes.post("/")
def create_job(body:JobSchema,request:Request,db:Session=Depends(get_db)):
    recruiter = recruiter_controller.is_recruiter_authenticated(request, db)
    return controller.create_job(body,db,recruiter)

@job_routes.get("/")
def get_jobs(db:Session=Depends(get_db)):
    return controller.get_jobs(db)

@job_routes.get("/YourJob/{job_id:int}")
def Job_By_Id(job_id:int,db:Session=Depends(get_db)):
    return controller.Job_By_Id(job_id,db)


@job_routes.put("/update/{job_id:int}")
def update_job(body:JobUpdateSchema,job_id:int,request:Request,db:Session=Depends(get_db)):
    recruiter = recruiter_controller.is_recruiter_authenticated(request, db)
    return controller.update_job(body,job_id,db,recruiter)


@job_routes.delete("/delete_job/{job_id:int}")
def delete_job(job_id:int,request:Request,db:Session=Depends(get_db)):
    recruiter = recruiter_controller.is_recruiter_authenticated(request, db)
    return controller.delete_job(job_id,db,recruiter)


@job_routes.get("/myJobs")
def get_my_jobs(request: Request,db: Session = Depends(get_db)):
    recruiter = recruiter_controller.is_recruiter_authenticated(request, db)
    return controller.get_my_jobs(db, recruiter)